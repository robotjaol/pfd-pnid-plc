# Factory I/O and CODESYS Setup

## Recommended Baseline

Use CODESYS V3.5 SP16 or later with CODESYS Control Win V3 and Factory I/O Modbus TCP/IP Client.

The current Factory I/O documentation provides a CODESYS Modbus TCP setup path and a downloadable sample for SP16 or higher.

## 1. Factory I/O Scene

1. Open `Sorting by Height (Advanced)`.
2. Save a copy under My Scenes because included scenes are read only.
3. Add these operator devices to the copied scene:
   1. Start Push Button NO
   2. Stop Push Button NC
   3. Reset Push Button NO
   4. Emergency Stop NC or equivalent simulated NC control
   5. Auto selector or maintained digital control
   6. Green Run lamp
   7. Red Fault lamp
   8. Auto mode lamp
4. Keep the original process sensors and actuators.

## 2. CODESYS Project

1. Create a Standard Project.
2. Select `CODESYS Control Win V3`.
3. Select Ladder Diagram for `PLC_PRG`.
4. Add a Global Variable List named `FIO` and paste `plc/GVL_FIO.txt`.
5. Add a Global Variable List named `HMI` and paste `plc/GVL_HMI.txt`.
6. Add the local declaration from `plc/PLC_PRG_declaration.txt`.
7. Create the Ladder networks in `plc/ladder-networks.md`.
8. Build the project.

## 3. Modbus TCP Device

Follow the current Factory I/O CODESYS Modbus setup pattern:

1. Add an Ethernet Adapter under the CODESYS device.
2. Add a Modbus TCP Slave Device under Ethernet.
3. Enable Discrete Bit Areas.
4. Allocate at least 32 writable Coil bits for Factory I/O sensor and operator input values.
5. Allocate at least 32 readable Discrete Input bits for PLC actuator and indication values.
6. Map GVL variables using the logical index order in `tag-map.csv`.
7. Start CODESYS Control Win V3.
8. Login, download, and run the PLC application.

## 4. Factory I/O Driver

1. Open File > Drivers.
2. Choose Modbus TCP/IP Client.
3. Set Host to the CODESYS runtime host. For a local runtime use `127.0.0.1`.
4. Use TCP port `502` unless the runtime configuration requires another port.
5. Use a Slave ID accepted by the installed CODESYS version. Factory I/O documentation specifically notes 0 or 255 for SP16.
6. Map sensors and buttons to the Coil indexes in `tag-map.csv`.
7. Configure Factory I/O digital actuator reads from the CODESYS Discrete Input area and map the output indexes in `tag-map.csv`.
8. Click Connect and confirm a green driver status.

## 5. First Commissioning

Do not immediately start automatic operation.

1. Monitor all FIO inputs online.
2. Manually move a Low box and High box through the classification sensors.
3. Confirm the polarity and sequence of `iLowBox` and `iHighBox`.
4. Verify `iAtLoadPos`, `iAtUnloadPos`, and `iAtFront` states.
5. Switch to Manual mode.
6. Jog each actuator one at a time.
7. Confirm Load and Unload directions.
8. Confirm Turn command behavior and return behavior.
9. Run the acceptance tests.

## Important

The Modbus mapping is a logical engineering map. Exact CODESYS device mapping presentation can differ slightly across service packs. Verify online values before starting the automatic sequence.
