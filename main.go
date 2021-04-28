//+build js,wasm

package main

import (
	"fmt"
	. "github.com/siongui/godom/wasm"
)

var (
	domains = map[string]string{
		"asciirange.com": "fas fa-bullseye",
		"cert.ist":       "fas fa-user-lock",
		"tilltrump.com":  "far fa-calendar-check",
		"urip.io":        "fas fa-code",
	}
	demos = map[string]string{
		"https://github.com/JBirdVegas/go-wasm-hello-world":   "Hello World",
		"https://github.com/JBirdVegas/jbird.dev/tree/golang": "This site",
	}
)

const (
	introText   = "jbird.dev"
	taglineText = "Stuff and things... Sometimes useful stuff and things"
	demosText   = "GoLang WASM demos..."
)

func createIconAndTextLink(text *string, domain, fontAwesomeIcon string) Value {
	a := Document.CreateElement("a")
	a.Set("target", "_blank")

	if text == nil {
		a.Set("href", fmt.Sprintf("https://%s", domain))
	} else {
		a.Set("href", domain)
	}
	aStyle := a.Get("style")
	aStyle.Set("display", "inline-block")
	aStyle.Set("padding", "50px")
	aStyle.Set("color", "#FAFAFA")

	i := Document.CreateElement("i")
	i.Set("className", fontAwesomeIcon)
	span := Document.CreateElement("span")
	if text == nil {
		span.Set("textContent", domain)
	} else {
		span.Set("textContent", *text)
	}
	span.Get("style").Set("display", "block")

	iStyle := i.Get("style")
	iStyle.Set("font-size", "3em")
	iStyle.Set("padding", "10px")

	a.Call("appendChild", i)
	a.Call("appendChild", span)

	return a
}

func setFavicon() {
	Document.QuerySelector("link[rel~='icon']").Set("href", "favicon.png")
}

func bodyCss() {
	bodyStyle := Document.Get("body").Get("style")
	bodyStyle.Set("font-family", "'Ubuntu Mono',monospace")
	bodyStyle.Set("backgroundColor", "#7e9733")
	bodyStyle.Set("color", "#FAFAFA")
	bodyStyle.Set("display", "flex")
	bodyStyle.Set("flex-direction", "column")
	bodyStyle.Set("min-height", "100vh")
	bodyStyle.Set("justify-content", "center")
	bodyStyle.Set("padding", "0 30px")
	bodyStyle.Set("margin-bottom", "-8%")
	bodyStyle.Set("text-align", "center")
}

func makeTitleDiv() Value {
	div := Document.CreateElement("div")
	div.Set("className", "intro")
	div.Set("textContent", introText)
	style := div.Get("style")
	style.Set("font-size", "3.75em")
	style.Set("font-weight", "600")
	return div
}

func makeTaglineDiv(text string) Value {
	div := Document.CreateElement("div")
	div.Set("className", "tagline")
	div.Set("textContent", text)
	style := div.Get("style")
	style.Set("font-size", "1.5rem")
	style.Set("font-weight", "100")
	style.Set("margin", "1.5rem 0")
	return div
}

func makeContentIconsDiv() Value {
	div := Document.CreateElement("div")
	div.Set("className", "icons-social")
	style := div.Get("style")
	style.Set("text-align", "center")
	style.Set("font-family", "'Ubuntu Mono',monospace")
	return div
}

func main() {
	setFavicon()
	bodyCss()

	contentIconsDiv := makeContentIconsDiv()
	for domain, icon := range domains {
		contentIconsDiv.Call("appendChild", createIconAndTextLink(nil, domain, icon))
	}

	demoIconsDiv := makeContentIconsDiv()
	for domain, label := range demos {
		demoIconsDiv.Call("appendChild", createIconAndTextLink(&label, domain, "fas fa-user-secret"))
	}

	mainDiv := Document.GetElementById("main")
	demoDiv := makeTaglineDiv(demosText)
	demoDiv.Get("style").Set("margin-bottom", "-4%")

	mainDiv.Call("appendChild", makeTitleDiv())
	mainDiv.Call("appendChild", makeTaglineDiv(taglineText))
	mainDiv.Call("appendChild", contentIconsDiv)
	mainDiv.Call("appendChild", demoDiv)
	mainDiv.Call("appendChild", demoIconsDiv)
}
