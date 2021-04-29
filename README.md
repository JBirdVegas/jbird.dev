### A simple webpage with Go and WASM

Compile via:

`GOARCH=wasm GOOS=js go build -ldflags="-s -w" -o compiled/jbird.dev.wasm .`

Once this is compiled load `index.html` in a browser

[See a live demo here.](https://jbirdvegas.github.io/jbird.dev/)
