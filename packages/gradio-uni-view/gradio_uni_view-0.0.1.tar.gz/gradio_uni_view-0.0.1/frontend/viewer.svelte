<svelte:options accessors={true} />

<script lang="ts">
    import type { Gradio } from "@gradio/utils";
    import { Block } from "@gradio/atoms";
    import type { LoadingStatus } from "@gradio/statustracker";
    import { tick } from "svelte";
    import {
        Granularity,
        LightPlugin,
        Color,
        RepresentationType,
        AtomReprType,
        MolecularReprType,
    } from "dpmol";

    export let gradio: Gradio<{
        change: never;
        submit: never;
        input: never;
        clear_status: LoadingStatus;
    }>;
    export let value = "";
    export let height;
    export let structures: any[] = [];

    window.process = {
        env: {
            NODE_ENV: "production",
            LANG: "",
        },
    };

    let lightPlugin = new LightPlugin();

    const guid = () => {
        function S4() {
            // eslint-disable-next-line no-bitwise
            return (((1 + Math.random()) * 0x10000) | 0)
                .toString(16)
                .substring(1);
        }
        return `${S4() + S4()}-${S4()}-${S4()}-${S4()}-${S4()}${S4()}${S4()}`;
    };
    const key = guid();
    $: key;

    let el: HTMLTextAreaElement | HTMLInputElement;
    const container = true;

    function handle_change(): void {
        gradio.dispatch("change");
    }

    async function handle_keypress(e: KeyboardEvent): Promise<void> {
        await tick();
        if (e.key === "Enter") {
            e.preventDefault();
            gradio.dispatch("submit");
        }
    }

    $: if (value === null) value = "";

    // When the value changes, dispatch the change event via handle_change()
    // See the docs for an explanation: https://svelte.dev/docs/svelte-components#script-3-$-marks-a-statement-as-reactive
    $: value, handle_change();

    let info = "";

    const updateInfo = () => {
        const label = document.getElementById(`uni-view-label-${key}`)
        if (!label) return
        if (!info) {
            label.style.display = 'none'
            return;
        }
        label.innerHTML = info;
        label.style.display = 'block';
    }

    $: info, updateInfo();
    const init = () => {
        lightPlugin.managers.representation.showPolarHydrogenOnly = false;
        // 修改光照及hover select颜色
        lightPlugin.createCanvas(
            document.getElementById(`uni-view-canvas-${key}`),
            {
                renderer: {
                    ambientIntensity: 0.4,
                    backgroundColor: Color(0xf2f5fa),
                },
            },
        );
        lightPlugin.managers.highlight.info.subscribe((data) => {
            if (!data.info) {
                info = "";
                return;
            }
            if (data.info.type === "Structure") {
                const {
                    granularity,
                    atomName,
                    atomId,
                    altId,
                    residueName,
                    residueId,
                    chainId,
                    emConfidence,
                    bfactor,
                    insertCode,
                    ref,
                } = data.info;
                const molecularName = lightPlugin.managers.cell.getMolecularName(ref)
                switch (granularity) {
                    case "Atom":
                        info = `${molecularName ? `${molecularName} ` : ''}${atomName} ${atomId}${altId} ${residueName} ${residueId}${insertCode ?? ""} ${chainId}${
                            bfactor ? `<p />b-factor: ${bfactor}` : ""
                        }${emConfidence ? `<p />EM Confidence: ${emConfidence}` : ""}`;
                        break;
                    case "Residue":
                        info = `${molecularName ? `${molecularName} ` : ''}${residueName} ${residueId}${
                            insertCode ?? ""
                        } ${chainId}${bfactor ? `<p />b-factor: ${bfactor}` : ""}`;
                        break;
                    case "Chain":
                        info = `${molecularName ? `${molecularName} ` : ''}Chain ${chainId}`;
                        break;
                    default:
                        info = `${molecularName ? `${molecularName} ` : ''}`;
                        break;
                }
                return;
            }
            if (data.info.type === "Interaction") {
                const { interactionType, infoA, infoB } = data.info;
                info = `${interactionType} ${infoA.chainId}:${infoA.residueName}${infoA.residueId}:${infoA.atomName} - ${infoB.chainId}:${infoB.residueName}${infoB.residueId}:${infoB.atomName}`;
                return;
            }
            info = "";
        });
        // @ts-ignore
        // eslint-disable-next-line no-underscore-dangle
        window.__simple_plugin = lightPlugin;
        setTimeout(() => lightPlugin.refresh(), 50);
        handleStructures();
    };
    const interval = setInterval(() => {
        if (
            document.getElementById(`uni-view-canvas-${key}`) &&
            !lightPlugin.canvas3d
        ) {
            clearInterval(interval);
            init();
        }
    }, 1000);
    const resize = () => {
        setTimeout(() => {
            lightPlugin.refresh({ fixCamera: true });
        }, 0);
    };
    $: height, resize();
    const colorHexToNumber = (color = "#F2F5FA") => {
        if (color.startsWith("#")) {
            color = color.substr(1);
        }
        return parseInt(color, 16);
    };
    const handleStructures = () => {
        lightPlugin.clear();
        if (!lightPlugin.canvas3d) return;
        structures.forEach((item) => {
            // carbon color预置部分颜色
            const { format, content, reprType, carbonColor } = item;
            if (!MolecularReprType.has(reprType) || !content) return;
            lightPlugin.managers.representation.createMolecular({
                format,
                data: content,
                reprType:
                    reprType ??
                    (format === "pdb"
                        ? RepresentationType.Ribbon
                        : RepresentationType.BallAndStick),
                theme:
                    carbonColor && AtomReprType.has(reprType)
                        ? {
                              Atom: {
                                  color: {
                                      name: "element-symbol",
                                      props: {
                                          carbonColor: {
                                              name: "uniform",
                                              params: {
                                                  value: Color(
                                                      colorHexToNumber(
                                                          carbonColor,
                                                      ),
                                                  ),
                                              },
                                          },
                                      },
                                  },
                              },
                          }
                        : undefined,
            });
        });
    };

    $: structures, handleStructures();
</script>

<div
    class="uni-view-container"
    style={height !== undefined ? `height: ${height}px;` : ""}
>
    <div id="uni-view-canvas-{key}" class="uni-view-canvas"></div>
    <div class="uni-view-toolbar">
        <button
            class="uni-view-toolbar-btn"
            on:click={() => lightPlugin.managers.camera.zoomIn()}
        >
            <svg
                width="1em"
                height="1em"
                viewBox="0 0 16 16"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                    d="M8.02 3.334l-.012 9.333M3.336 8h9.333"
                    stroke="#A2A5C4"
                    stroke-width="1.3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />
            </svg>
        </button>
        <button
            class="uni-view-toolbar-btn"
            on:click={() => lightPlugin.managers.camera.zoomOut()}
        >
            <svg
                width="1em"
                height="1em"
                viewBox="0 0 16 16"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                    d="M3.336 8h9.333"
                    stroke="#A2A5C4"
                    stroke-width="1.3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />
            </svg>
        </button>
        <button
            class="uni-view-toolbar-btn"
            on:click={() => lightPlugin.managers.camera.focus()}
        >
            <svg
                width="1em"
                height="1em"
                viewBox="0 0 16 16"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
            >
                <path
                    d="M8.0026 14.6673C11.6845 14.6673 14.6693 11.6825 14.6693 8.00065C14.6693 4.31875 11.6845 1.33398 8.0026 1.33398C4.32071 1.33398 1.33594 4.31875 1.33594 8.00065C1.33594 11.6825 4.32071 14.6673 8.0026 14.6673Z"
                    stroke="#A2A5C4"
                    stroke-width="1.3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />
                <path
                    d="M8 12.334V14.6673"
                    stroke="#A2A5C4"
                    stroke-width="1.3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />
                <path
                    d="M12 8H14.6667"
                    stroke="#A2A5C4"
                    stroke-width="1.3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />
                <path
                    d="M1.33594 8H3.66927"
                    stroke="#A2A5C4"
                    stroke-width="1.3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />
                <path
                    d="M8 3.66732V1.33398"
                    stroke="#A2A5C4"
                    stroke-width="1.3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                />
                <circle cx="8" cy="8" r="1" stroke="#A2A5C4" />
            </svg>
        </button>
    </div>
    <div
        id="uni-view-label-{key}"
        class="uni-view-label"
        style="display: none;"
    />
</div>

<style>
    .uni-view-container {
        width: 100%;
        height: 100%;
        position: relative;
        min-height: 240px;
    }
    .uni-view-canvas {
        width: 100%;
        height: 100%;
        min-height: 240px;
    }
    .uni-view-toolbar {
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        display: flex;
        flex-direction: column;
        color: #000000;

        background: #ffffff;
        box-shadow:
            0 6px 10px rgba(183, 192, 231, 0.1),
            0 8px 12px 1px rgba(170, 181, 223, 0.05);
        border-radius: 4px;
        padding: 4px;
        margin-bottom: 8px;
    }
    .uni-view-toolbar-btn {
        cursor: pointer;
        font-size: 16px;
        height: 16px;
        width: 16px;
        margin-bottom: 4px;
    }
    .uni-view-toolbar-btn:hover {
        cursor: pointer;
        color: #555878;
    }
    .uni-view-label {
        background: #555878;
        opacity: 0.8;
        border-radius: 4px;
        color: #FFFFFF;
        position: absolute;
        left: 0px;
        bottom: 0px;
        z-index: 999;
        padding: 4px 8px;
        bottom: 0;
    }
</style>
