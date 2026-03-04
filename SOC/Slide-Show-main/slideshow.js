const slideImg = document.getElementById("slide");
const prev = document.getElementById("prev");
const next = document.getElementById("next");
const startBtn = document.getElementById("start");
const stopBtn = document.getElementById("stop");
const saveBtn = document.getElementById("saveJson");

let raw = sessionStorage.getItem("slideshowData");

let slides = [];
let delay = 5000;

if (raw) {
  try {
    let data = JSON.parse(raw);
    slides = data.slides || [];
    delay = data.delay || 5000;
  } catch {
    slides = [];
  }
}

let index = 0;
let timer = null;

function show() {
  if (!slides.length) return;
  slideImg.src = slides[index];
}

function nextSlide() {
  index = (index + 1) % slides.length;
  show();
}

function prevSlide() {
  index = (index - 1 + slides.length) % slides.length;
  show();
}

function start() {
  stop();
  timer = setInterval(nextSlide, delay);
}

function stop() {
  clearInterval(timer);
}

prev.onclick = prevSlide;
next.onclick = nextSlide;
startBtn.onclick = start;
stopBtn.onclick = stop;

saveBtn.onclick = () => {
  const blob = new Blob([JSON.stringify({ slides, delay })], {
    type: "application/json"
  });
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "slideshow.json";
  a.click();
};

show();
start();