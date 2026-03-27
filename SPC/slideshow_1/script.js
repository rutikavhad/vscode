
const upload = document.getElementById("upload");
const gallery = document.getElementById("gallery");
const deleteBtn = document.getElementById("deleteSelected");
const slideBtn = document.getElementById("slideshowSelected");
const slideTimeInput = document.getElementById("slideTime");
const loadJson = document.getElementById("loadJson");

const preview = document.getElementById("preview");
const previewImg = document.getElementById("previewImg");

let photos = [];
let selected = new Set();
let counts = {}; // image index repeat count
let dragFrom = null;

// Upload Base64 instead of blob UR
upload.addEventListener("change", e => {
  [...e.target.files].forEach(file => {
    const reader = new FileReader();
    reader.onload = ev => {
      photos.push(ev.target.result); //Base64
      renderGallery();
    };
    reader.readAsDataURL(file);
  });
});

// Render
function renderGallery() {
  gallery.innerHTML = "";
  selected.clear();
  counts = {};

  photos.forEach((src, i) => {
    counts[i] = 1;

    const card = document.createElement("div");
    card.className = "photo-card";
    card.draggable = true;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "select";

    const img = document.createElement("img");
    img.src = src;

    const controls = document.createElement("div");
    controls.className = "count-controls";
    controls.innerHTML = `
      <button>-</button>
      <span>1</span>
      <button>+</button>
    `;

    const [minus, span, plus] = controls.children;

    minus.onclick = () => {
      if (counts[i] > 1) span.textContent = --counts[i];
    };
    plus.onclick = () => span.textContent = ++counts[i];

    checkbox.onchange = () => {
      checkbox.checked ? selected.add(i) : selected.delete(i);
    };

    img.onclick = () => {
      previewImg.src = src;
      preview.style.display = "flex";
    };

    card.ondragstart = () => dragFrom = i;
    card.ondragover = e => e.preventDefault();
    card.ondrop = () => {
      [photos[dragFrom], photos[i]] = [photos[i], photos[dragFrom]];
      renderGallery();
    };

    card.append(checkbox, img, controls);
    gallery.appendChild(card);
  });
}

//Delete 
deleteBtn.onclick = () => {
  photos = photos.filter((_, i) => !selected.has(i));
  renderGallery();
};

//Slideshow 
slideBtn.onclick = () => {
  let list = [];
  [...selected].forEach(i => {
    for (let c = 0; c < counts[i]; c++) list.push(photos[i]);
  });

  sessionStorage.setItem(
    "slideshowData",
    JSON.stringify({
      slides: list,
      delay: slideTimeInput.value * 5000
    })
  );

  window.open("slideshow.html", "_blank");
};

// Load JSON 
loadJson.onchange = e => {
  const file = e.target.files[0];
  const reader = new FileReader();
  reader.onload = () => {
    sessionStorage.setItem("slideshowData", reader.result);
    window.open("slideshow.html", "_blank");
  };
  reader.readAsText(file);
};

// Preview Close 
preview.onclick = () => preview.style.display = "none";


const slideImg = document.getElementById("slide");
const prev = document.getElementById("prev");
const next = document.getElementById("next");
const startBtn = document.getElementById("start");
const stopBtn = document.getElementById("stop");
const saveBtn = document.getElementById("saveJson");
const slideshow = document.getElementById("slideshow");


let raw = sessionStorage.getItem("slideshowData");
let data = raw ? JSON.parse(raw) : { slides: [], delay: 5000 };

let slides = data.slides || [];
let delay = data.delay || 5000;

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
  const blob = new Blob(
    [JSON.stringify({ slides, delay })],
    { type: "application/json" }
  );
  const a = document.createElement("a");
  a.href = URL.createObjectURL(blob);
  a.download = "slideshow.json";
  a.click();
};


document.addEventListener("keydown", e => {
  if (!slides.length) return;

  if (e.key === "ArrowRight") nextSlide();
  if (e.key === "ArrowLeft") prevSlide();

  if (e.key.toLowerCase() === "f") {
    if (!document.fullscreenElement) {
      slideshow.requestFullscreen();
    } else {
      document.exitFullscreen();
    }
  }
});

show();
start();
