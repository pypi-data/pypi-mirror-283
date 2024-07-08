#!/usr/bin/python3

from emmi.api.exports import ConnectorKinds, SignalConnector, ActorConnector, \
    PropertyConnector

import logging, asyncio
logger = logging.getLogger(__name__)

class MotorConnector(object):
    '''
    Implements a simple EPICS motor record, with a small subset of the
    [EPICS motor record](https://epics.anl.gov/bcda/synApps/motor/R7-1/motorRecord.html)
    variables. Relies on a motor inteface as described by `MotorEngine`, i.e.
    a class with the following properties:

      - `position`: returns the current motor values, respectively moves
        to the specified relative value

      - `position_relative`: facilitates a movement relative to the current
        position

      - `state`: a string that begins with one of the following:
    
          - "INIT" (preparing to take commands)
    
          - "IDLE" (not moving, ready to take commands)

          - "STAGING" (about to enter BUSY, but not all BUSY makers are present yet)
    
          - "BUSY" (not able to accept commands, most likely already moving)
    
          - "ERROR" (stopped, reached a situation which requires external action)

          - "STOP" (stopping)
    
          - "FAIL" (unefined state, best effort to be stopped, unrecoverable error)
    
        The state string is intentionally checked only for its beginning part.
        States may be explicitly extended by appending information to strings,
        e.g. "BUSY.TRACKING" or "BUSY.HOMING" to distinguish different flavors
        of states. `SimpleMotor` will not react to anything beyond the five
        1st-level state information, but other software layers may.

    This class needs to be used with a
    [pythonSoftIOC](https://dls-controls.github.io/pythonSoftIOC)
    compatible EPICS IOC Python API. It uses `asyncio` for all asynchronous
    work.

    It implements the EPICS motor record variables VAL, RBV, RVL, HOMF/HOMB,
    STOP.

    FIXME: need to add support for supplementary actions / properties / signals
    (e.g. extend by additional "BUSY" states, or read/write specific properties
    like limits, force probe thresholds etc).
    '''    

    def __init__(self, motor_prefix, motor_engine, ioc_dispatcher,
                 poll_period=0.1, separator="_"):
        '''
        Initializes the IOC variables. Parameters:
        
          - `motor_prefix`: a string to prepend to the motor variables.
        
          - `motor_engine`: the `MotorEngine` object we'll be talking to.
        
          - `ioc_dispatcher`: a pythonSoftIOC asyncio dispatcher compatible
            instance (typically a `softioc.asyncio_dispatcher.AsyncioDispatcher()`)
        '''

        self.pollPeriod = poll_period

        #from softioc import builder as ioc_builder

        # SPEC needs the following:
        #
        # Can be ignored / business of the controller?
        #  o ACCL: acceleration time in seconds (0.0)
        #  o BDST: backlash distance egu (0)
        #  o BVAL: backlash velocity egu/s (0)
        #  o VBAS: base velocity (minimum velocity?) egu/s (0)
        #  o ERES: encoder step size egu (0)
        #  o MRES: motor step size egu (0)
        #
        # Calibration fields and coordinate system transformations:
        #  - SET: set/use switch for calibration fields (0: use, 1: set)
        #  - FOFF: offset freeze switch -- is the user prevented from
        #          writing the offset?
        #  - OFF: user offset egu
        #  + DIR: user direction        
        #  - RRBV: raw readback value
        #  - RVAL: raw desired value        
        #
        # Unclear:
        #  o UEIP: use encoder if present (always 1?)
        #  o VELO: velocity egu/s (set to 0?)
        #
        # Need to have / already have:
        #  o STOP: stop
        #  o VAL: user desired value
        #  - SPMG: stop/pause/move/go -- complicated beast
        #    - Stop: same as STOP?        
        #
        # Nice to have, but not part of the EDA Motor Model:
        #  + DHLM: dial high-limit
        #  + DLLM: dial low-limit
        #  + HLS: at high-limit switch
        #  + LLS: at low-limit switch        
        #  o DMOV: done moving to value
        #
        # Unknown:
        #  + DISP: disable (turn off motor/unusable)        
        #
        # Nice to have, not needed by SPEC:
        #  o EGU: engineering unit names
        #  - RLV: relative-move value: when changed, changes VAL,
        #    then resets itself to 0
        #  
        
        self.engine = motor_engine

        # VAL/RBV
        self.con_pos = PropertyConnector(ioc_dispatcher,
                                         suffix=motor_prefix+separator,
                                         access=self.motor_position,
                                         signal={ 'pollPeriod': poll_period },
                                         kind="analog")

        # STATE (motor engine)
        self.con_state = SignalConnector(ioc_dispatcher,
                                         suffix=motor_prefix+separator+"STATE",
                                         access=(motor_engine, "state"),
                                         pollPeriod=poll_period,
                                         kind="strings",
                                         validator={ 'values': [
                                             'INIT', 'IDLE', 'STAGING', 'BUSY',
                                             'STOP', 'ERROR', 'FATAL'
                                         ]})

        # STOP
        self.con_stop = ActorConnector(ioc_dispatch=ioc_dispatcher,
                                       suffix=motor_prefix+separator+"STOP",
                                       access=self.conExecStop,
                                       kind="values",
                                       validator={'values': [0, 1]})

        self.motor_name = motor_prefix
        self.motor_prefix = motor_prefix
        self.prefix_separator = separator

        # for use with .addBusy()
        self.additional_actions = {}

        self.ioc_dispatcher = ioc_dispatcher


    def motor_position(self, val=None):
        print("pos!")
        if val is None:
            return self.engine.position
        else:
            self.engine.position = val


    def addBusy(self, action_suffix, go, **go_params):
        '''
        Adds an additional motor work trigger with the specified suffix.
        
        Some motors support additional actions in their BUSY phase (e.g.
        relative move, homing action etc). This supports a simple extension
        mechanism which takes a EPICS variable suffix (e.g. "HOMF") and
        a set of parameters for the `MotorEngine.go()` function.
        '''

        class MarkGoUnmark:
            def __init__(self, go_name, go_params, engine, marker_pv):
                self.go_name = go_name
                self.go_params = go_params
                self.engine = engine
                self.marker_pv = marker_pv
            
            # wrapper to mark
            async def __call__(self, val):

                if val == 0:
                    logger.debug(f'{self.go_name}: val={val} requested, nothing to do')
                    return

                logger.debug(f'{self.go_name}: triggered, val={val}')
                logger.debug(f"Requesting BUSY/{self.go_name}")

                # triggering action
                self.engine.go(self.go_name, **self.go_params)

                # ...wait for action to start...
                while self.engine.state != 'BUSY':
                    await asyncio.sleep(0.1)

                # ...then wait for action to finish
                while True:
                    if (self.engine.state != "BUSY") or \
                       (self.engine.state == "BUSY") and (self.engine.business != self.go_name):
                        logger.debug(f"State: {self.engine.state}, business: {self.engine.business}")
                        logger.info(f"Done with BUSY/{self.go_name}")
                        break
                    await asyncio.sleep(0.1)
                
                try:
                    logger.debug(f'{self.go_name}: done, removing mark')
                    self.marker_pv.pv.set(0)

                except Exception as e:
                    # this happens on Raspi
                    logger.error(f'{self.go_name}: done, but val=0 update failed')


        thing_doer = MarkGoUnmark(go, go_params, self.engine, None)
        self.additional_actions[action_suffix] = \
            ActorConnector(self.ioc_dispatcher,
                           suffix=self.motor_prefix+self.prefix_separator+action_suffix,
                           access=thing_doer,
                           kind="integer")
        
        thing_doer.marker_pv = self.additional_actions[action_suffix]


    async def conExecStop(self, val):
        '''
        EPICS motor STOP command: if val==1, it executes the STOP command,
        then it sets VAL to current position and resets itself to 0.
        '''
        if val != 1:
            return

        self.engine.state = "STOP"
        self.con_stop.pv.set(0)
        
        while self.engine.state != "IDLE":
            await asyncio.sleep(self.pollPeriod)
            
        self.con_val.set(self.engine.position)


class DMOVMixin:
    ''' Implements the DMOV motor suffix (returns 1 while motor is not IDLE).
    '''
    def __init__(self):
        
        # DMOV - set to 0 when motor begins moving
        self.con_dmov = SignalConnector(self.ioc_dispatcher,
                                        suffix=self.motor_prefix+self.prefix_separator+"DMOV",
                                        access=lambda: int(self.engine.state == "IDLE"),
                                        kind="integer",
                                        pollPeriod=self.pollPeriod)


class MSTAMixin:
    ''' Implements a SPEC-like STATUS motor suffix (returns 0x02 bit set while moving).

    EPICS (motor record) actually defines the following bits:
      1. DIRECTION: last raw direction; (0:Negative, 1:Positive)
      2. DONE: motion is complete.
      3. PLUS_LS: plus limit switch has been hit.
      4. HOMELS: state of the home limit switch.
      5. Unused
      6. POSITION: closed-loop position control is enabled.
      7. SLIP_STALL: Slip/Stall detected (eg. fatal following error)
      8. HOME: if at home position.
      9. PRESENT: encoder is present.
     10. PROBLEM: driver stopped polling, or hardware problem
     11. MOVING: non-zero velocity present.
     12. GAIN_SUPPORT: motor supports closed-loop position control.
     13. COMM_ERR: Controller communication error.
     14. MINUS_LS: minus limit switch has been hit.
     15. HOMED: the motor has been homed.
    '''

    def __init__(self):
        
        suffix=self.motor_prefix+self.prefix_separator+"MSTA"
        
        status_lambda = lambda: 0x02 if self.engine.state == "BUSY" else 0x00
        
        self.con_status = SignalConnector(self.ioc_dispatcher,
                                          suffix=suffix,
                                          access=status_lambda,
                                          kind="integer",
                                          pollPeriod=self.pollPeriod)


class CalibrationMixin:
    '''
    Adds calibration and user/dial coordinate transformation functionality.
    If you add this to your motor, the `.position` property will, in fact,
    return "user" coordinates, which differ from the "dial" coordinates
    (i.e. the raw output of `Motor.where()`) by the equation
    `user = dial*dir + offs`.
    
    These will be exposed via `VAL` / `RBV`.

    The raw output of `.where()` will actually be exposed
    in `DVAL` / `DRBV` / `DMOV`.

    Additional variables will be added:
     - `DIR` for direction
     - `OFF` for offset
     - `FOFF` to freeze / unfreeze offset (always `0`, i.e. "variable")
     - `SET` / `SSET` / `SUSE`
    '''
    
    def __init__(self, offset=0, direction=1):
        self._usr_offset = offset
        self._usr_direction = direction

        self.con_dial_pos = PropertyConnector(self.ioc_dispatcher,
                                              suffix=f'{self.motor_prefix}{self.prefix_separator}D',
                                              access=self.dial_motor_position,
                                              signal={ 'pollPeriod': self.pollPeriod },
                                              kind="analog")


        self.con_offs = ActorConnector(ioc_dispatch=self.ioc_dispatcher,
                                       suffix=self.motor_prefix+self.prefix_separator+"OFF",
                                       access=self.user_offset,
                                       kind="analog")


        self.con_dir = ActorConnector(ioc_dispatch=self.ioc_dispatcher,
                                      suffix=self.motor_prefix+self.prefix_separator+"DIR",
                                      access=self.user_direction,
                                      kind="analog")

        # EMMI doesn't (yet) explicitly support "r/w actors". Actors are write-only (from
        # the EPICS user's perspective).
        # But there's nothing wrong with setting a PV from this side of the code, we just
        # have to do it explicitly. And in particular, we have to do this for the
        # initialization.
        self.con_offs.pv.set(self._usr_offset)
        self.con_dir.pv.set(self._usr_direction)
        

    def user_offset(self, val=None):
        # Used primarily to set the user offset from the EPICS side, through PVs
        if val is None:
            return self._usr_offset
        else:
            self._usr_offset = val


    def user_direction(self, val=None):
        # Used to set direction (0=pos, 1=neg), to EPICS conventions.
        # Returns the mathematical direction (i.e. -1 / +1, depending
        # on the ._usr_direction field)
        if val is None:
            return { 0: 1, 1: -1}[self._usr_direction]
        else:
            self._usr_direction = val


    def dial_motor_position(self, val=None):
        if val is None:
            return self.engine.position
        else:
            self.engine.position = val


    def user_motor_position(self, val=None):
        if val is None:
            return self.dial_motor_position()*self.user_direction() + self._usr_offset
        else:
            self.dial_motor_position((val-self._usr_offset)/self.user_direction())


    def motor_position(self, val=None):
        # Hijacking the .motor_position() of the parent class to
        # actually display the user-position instead of the original
        # hardware position
        return self.user_motor_position(val)


class ErrorMixin:
    ''' Adds error read / clear functionality '''
    def __init__(self):
        self.con_eclr = ActorConnector(ioc_dispatch=self.ioc_dispatcher,
                                       suffix=self.motor_prefix+self.prefix_separator+"ECLR",
                                       access=self.clear_motor,
                                       kind="values",
                                       validator={'values': [0, 1]})

    def clear_motor(self, val):
        if val > 0:
            self.engine.clear_motor()
            self.con_eclr.pv.set(0)
        
        
    
        
class SpecMixin:
    ''' Adds a number of nonsensical fields to keep Spec happy '''

    def __init__(self):
        
        # lots of variables expected by spec but which we don't really serve
        self.con_constants = [
            SignalConnector(self.ioc_dispatcher,
                            suffix=self.motor_prefix+self.separator_suffix+s,
                            access=lambda: value,
                            kind=kind,
                            pollPeriod=10.0)
            for s,kind,value in [ ("ACCL", "analog", 0),
                                  ("BDST", "analog", 0),
                                  ("BVAL", "analog", 0),
                                  ("VBAS", "analog", 0),
                                  ("ERES", "analog", 0),
                                  ("MRES", "analog", 0),
                                  ("UEIP", "analog", 1),
                                  ("VELO", "analog", 0)]]
        #("EGU",  "text", "mm")] ]
