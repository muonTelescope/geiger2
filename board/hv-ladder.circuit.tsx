/** Review schematic of the simulated CW ladder. Not a fabrication board. */
export default () => (
  <board routingDisabled>
    <chip name="U1" schX={-5} schY={2}
      pinLabels={{pin1:'SW',pin2:'GND'}}
      schPinArrangement={{leftSide:['GND'],rightSide:['SW']}} />
    {Array.from({length:4},(_,i)=>{
      const n=i+1, x=i*6
      const prevP=i===0?'SW':`P${i}`, prevS=i===0?'GND':`S${i}`
      return <group key={n}>
        <capacitor name={`C${2*n-1}`} capacitance="10nF" footprint="1206" schX={x} schY={4}
          connections={{pin1:`net.${prevP}`,pin2:`net.P${n}`}} />
        <diode name={`D${2*n-1}`} footprint="sod123" schX={x-1.5} schY={2} schRotation={90}
          connections={{anode:`net.${prevS}`,cathode:`net.P${n}`}} />
        <diode name={`D${2*n}`} footprint="sod123" schX={x+1.5} schY={2} schRotation={270}
          connections={{anode:`net.P${n}`,cathode:`net.S${n}`}} />
        <capacitor name={`C${2*n}`} capacitance="10nF" footprint="1206" schX={x} schY={0}
          connections={{pin1:`net.${prevS}`,pin2:`net.S${n}`}} />
      </group>
    })}
    <trace from=".U1 > .SW" to="net.SW" />
    <trace from=".U1 > .GND" to="net.GND" />
    <resistor name="R1" resistance="33M" footprint="1206" schX={24} schY={4} connections={{pin1:'net.S4',pin2:'net.DIV1'}} />
    <resistor name="R2" resistance="33M" footprint="1206" schX={28} schY={4} connections={{pin1:'net.DIV1',pin2:'net.DIV2'}} />
    <resistor name="R3" resistance="33M" footprint="1206" schX={32} schY={4} connections={{pin1:'net.DIV2',pin2:'net.DIV3'}} />
    <resistor name="R4" resistance="33M" footprint="1206" schX={36} schY={4} connections={{pin1:'net.DIV3',pin2:'net.SENSE'}} />
    <resistor name="R5" resistance="412k" footprint="0603" schX={36} schY={0} schRotation={90} connections={{pin1:'net.SENSE',pin2:'net.GND'}} />
    <capacitor name="C9" capacitance="100pF" footprint="0603" schX={40} schY={0} schRotation={90} connections={{pin1:'net.SENSE',pin2:'net.GND'}} />
    <schematictext text="FOUR-STAGE CW / EIGHT DIODES / EIGHT 10 nF CAPACITORS" schX={9} schY={7} fontSize={0.7} />
    <schematictext text="SIMULATION REVIEW ONLY - SW drive and control in converter.cir" schX={16} schY={-4} fontSize={0.65} />
  </board>
)
