function run() {
    const asm = document.getElementById("asm").value;

    fetch("/run", {
        method: "POST",
        headers: { "Content-Type": "text/plain" },
        body: asm
    })
    .then(r => r.text())
    .then(t => document.getElementById("out").textContent = t)
    .catch(e => alert(e));
}
