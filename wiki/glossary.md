# Engineering Glossary & Definitions

This glossary serves as the absolute technical reference to define all terms, abbreviations, and layout parameters used across this project's documentation.

- **SDFS (Smart Digital File System):** A proprietary, flat binary partition allocation framework designed by Actions Semiconductor. It maps structural system resources using continuous, non-overlapping byte sectors instead of dynamic file cluster tables to preserve long-term flash stability on embedded devices.
- **AOTA:** A generic project-internal nickname used to describe the custom multi-image firmware container format discovered on this platform. The official manufacturer specification name remains currently unverified.
- **Zephyr RTOS:** A scalable, open-source real-time operating system optimized for resource-constrained, embedded systems. It uses clear symbol structures, modular memory footprints, and strict driver abstraction layers.
- **extcfg.bin (Extended Configuration Table):** An uncompressed binary configuration layout file managed inside the SDFS container structure. It directly holds peripheral parameters, register definitions, display bus clock selections, and chip driver limits used at boot time.
- **usrcfg.bin (User Configuration Table):** An uncompressed configuration block within the SDFS that holds non-volatile operational flags, user interface state data, and default preference matrices.
- **DMA (Direct Memory Access):** A hardware system peripheral mechanism that allows embedded subsystems to read or write memory bytes directly without passing those transactions through the primary CPU core, essential to maintain high display refresh streams.