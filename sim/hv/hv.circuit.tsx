import { hvModel } from './model'
/** Exploratory closed-loop HV model. Footprint is a simulation symbol only. */
export default () => (
  <board routingDisabled>
    <voltagesource name="VBAT" voltage="2.4V" schX={-6} schY={0} />
    <chip name="HV" footprint="soic8" schX={0} schY={0}
      pinLabels={{pin1:"battery", pin2:"GND", pin3:"hv",pin4:"sw",pin5:"sense"}}
      spiceModel={<spicemodel source={hvModel} />} />
    <trace from=".VBAT > .pin1" to=".HV > .battery" />
    <trace from=".VBAT > .pin2" to=".HV > .GND" />
    <voltageprobe name="HV_OUT" connectsTo=".HV > .hv" />
    <voltageprobe name="SWITCH" connectsTo=".HV > .sw" />
    <voltageprobe name="HV_SENSE" connectsTo=".HV > .sense" />
    <analogsimulation duration="150ms" timePerStep="2us" spiceEngine="ngspice" />
  </board>
)
