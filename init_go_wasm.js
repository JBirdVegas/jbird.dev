const go = new Go();
let module, instance;
WebAssembly.instantiateStreaming(
    fetch("compiled/jbird.dev.wasm", {cache: 'no-cache'}), go.importObject).then((result) => {
    module = result.module;
    instance = result.instance;
    run();
});

async function run() {
    await go.run(instance);
}