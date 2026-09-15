import { Fragment } from "react"
/** Review schematic of the simulated CW ladder. Not a fabrication board. */
const nodePorts: Record<string, string[]> = {
 SW:['.U1 > .SW','.C1 > .pin1'],
 GND:['.U1 > .GND','.D1 > .anode','.C2 > .pin1','.R5 > .pin2','.C9 > .pin2'],
 P1:['.C1 > .pin2','.D1 > .cathode','.D2 > .anode','.C3 > .pin1'],
 S1:['.D2 > .cathode','.C2 > .pin2','.D3 > .anode','.C4 > .pin1'],
 P2:['.C3 > .pin2','.D3 > .cathode','.D4 > .anode','.C5 > .pin1'],
 S2:['.D4 > .cathode','.C4 > .pin2','.D5 > .anode','.C6 > .pin1'],
 P3:['.C5 > .pin2','.D5 > .cathode','.D6 > .anode','.C7 > .pin1'],
 S3:['.D6 > .cathode','.C6 > .pin2','.D7 > .anode','.C8 > .pin1'],
 P4:['.C7 > .pin2','.D7 > .cathode','.D8 > .anode'],
 S4:['.D8 > .cathode','.C8 > .pin2','.R1 > .pin1'],
 DIV1:['.R1 > .pin2','.R2 > .pin1'],
 DIV2:['.R2 > .pin2','.R3 > .pin1'],
 DIV3:['.R3 > .pin2','.R4 > .pin1'],
 SENSE:['.R4 > .pin2','.R5 > .pin1','.C9 > .pin1'],
}
export default () => (
  <board routingDisabled schTraceAutoLabelEnabled={false}>
    <chip name="U1" schX={-5} schY={2}
      pinLabels={{pin1:'SW',pin2:'GND'}}
      schPinArrangement={{leftSide:['GND'],rightSide:['SW']}} />
    {Array.from({length:4},(_,i)=>{
      const n=i+1, x=i*6
      return <Fragment key={n}>
        <capacitor name={`C${2*n-1}`} capacitance="10nF" footprint="1206" schX={x} schY={4} />
        <diode name={`D${2*n-1}`} footprint="sod123" schX={x-1.5} schY={2} schRotation={90} />
        <diode name={`D${2*n}`} footprint="sod123" schX={x+1.5} schY={2} schRotation={270} />
        <capacitor name={`C${2*n}`} capacitance="10nF" footprint="1206" schX={x} schY={0} />
      </Fragment>
    })}

    <resistor name="R1" resistance="33M" footprint="1206" schX={3} schY={-5} />
    <resistor name="R2" resistance="33M" footprint="1206" schX={7} schY={-5} />
    <resistor name="R3" resistance="33M" footprint="1206" schX={11} schY={-5} />
    <resistor name="R4" resistance="33M" footprint="1206" schX={15} schY={-5} />
    <resistor name="R5" resistance="412k" footprint="0603" schX={18} schY={-7} schRotation={270} />
    <capacitor name="C9" capacitance="100pF" footprint="0603" schX={22} schY={-7} schRotation={270} />
    {Object.entries(nodePorts).flatMap(([node,ports])=>ports.slice(1).map((port,i)=>(
      <trace key={`${node}-${i}`} from={ports[0]} to={port} schDisplayLabel={node} />
    )))}
    <schematictext text="FOUR-STAGE CW / EIGHT DIODES / EIGHT 10 nF CAPACITORS" schX={9} schY={6} fontSize={0.32} />
    <schematictext text="SIMULATION REVIEW ONLY - SW drive and control in converter.cir" schX={9} schY={-11} fontSize={0.28} />
  </board>
)
