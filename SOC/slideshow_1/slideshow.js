const slideImg = document.getElementById("slide");
const prev = document.getElementById("prev");
const next = document.getElementById("next");
const startBtn = document.getElementById("start");
const stopBtn = document.getElementById("stop");
const saveBtn = document.getElementById("saveJson");
const slideshow = document.getElementById("slideshow");

let { slides, delay } = JSON.parse(sessionStorage.getItem("slideshowData"));
let index = 0;
let timer = null;

function show() {
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



document.addEventListener("keydown", (e) => {
  if (!slides.length) return;

  if (e.key === "ArrowRight") {
    nextSlide();
  }

  if (e.key === "ArrowLeft") {
    prevSlide();
  }

  if (e.key.toLowerCase() === "f") {
    toggleFullscreen();
  }
});


function toggleFullscreen() {
  if (!document.fullscreenElement) {
    slideshow.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
}

show();
start();