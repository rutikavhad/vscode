const upload = document.getElementById("upload");
const gallery = document.getElementById("gallery");
const deleteBtn = document.getElementById("deleteSelected");
const slideBtn = document.getElementById("slideshowSelected");

const slideImg = document.getElementById("slide");
const prevBtn = document.getElementById("prev");
const nextBtn = document.getElementById("next");

const preview = document.getElementById("preview");
const previewImg = document.getElementById("previewImg");

const fullscreenBtn = document.getElementById("fullscreenBtn");
const slideshow = document.getElementById("slideshow");

let photos = [];
let selected = new Set();
let slideList = [];
let slideIndex = 0;
let dragFrom = null;

let slideTimer = null;
const SLIDE_DELAY = 5000; // 5 seconds


//upload multiple files
upload.addEventListener("change", e => {
  [...e.target.files].forEach(file => {
    photos.push(URL.createObjectURL(file));
  });
  renderGallery();
  upload.value = "";
});

// Render Gallery Multiple photo show without refresh
function renderGallery() {
  gallery.innerHTML = "";
  selected.clear();

  photos.forEach((src, i) => {
    const card = document.createElement("div");
    card.className = "photo-card";  //photos by photo-cards
    card.draggable = true;

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.className = "select";

    const img = document.createElement("img");
    img.src = src;

    checkbox.onchange = () => {
      checkbox.checked ? selected.add(i) : selected.delete(i);
    };

    img.onclick = () => {
      previewImg.src = img.src;
      preview.style.display = "flex";
    };

    card.ondragstart = () => dragFrom = i;

    card.ondragover = e => e.preventDefault();

    card.ondrop = () => {
      if (dragFrom === null || dragFrom === i) return;
      [photos[dragFrom], photos[i]] = [photos[i], photos[dragFrom]];
      dragFrom = null;
      renderGallery();
    };

    card.appendChild(checkbox);
    card.appendChild(img);
    gallery.appendChild(card);
  });
}

// Delete Selected 
deleteBtn.onclick = () => {
  photos = photos.filter((_, i) => !selected.has(i));
  renderGallery();
};

// Slideshow


slideBtn.onclick = () => {
  slideList = selected.size
    ? [...selected].map(i => photos[i])
    : [...photos];

  if (!slideList.length) return;

  slideIndex = 0;
  showSlide();

  clearInterval(slideTimer); // show next slide after 5 sec
  slideTimer = setInterval(nextSlide, 5000);
};

function nextSlide() {
  slideIndex = (slideIndex + 1) % slideList.length;
  showSlide();
}

nextBtn.onclick = nextSlide;

prevBtn.onclick = () => {
  slideIndex = (slideIndex - 1 + slideList.length) % slideList.length;
  showSlide();
};


function showSlide() {
  if (!slideList.length) return;
  slideImg.src = slideList[slideIndex];
}

nextBtn.onclick = () => {
  slideIndex = (slideIndex + 1) % slideList.length;
  showSlide();
};

prevBtn.onclick = () => {
  slideIndex = (slideIndex - 1 + slideList.length) % slideList.length;
  showSlide();
};

// Preview Close click anyware
preview.onclick = () => {
  preview.style.display = "none";
  previewImg.src = "";
};

document.addEventListener("keydown", e => {
  if (e.key === "Escape") preview.click();
});

// show slide show on full screen
fullscreenBtn.onclick = () => {
  if (!document.fullscreenElement) {
    slideshow.requestFullscreen();
  } else {
    document.exitFullscreen();
  }
};

//add keyboards button trigger
document.addEventListener("keydown", (e) => {
  if (!slideList.length) return;

  if (e.key === "ArrowRight") {
    nextBtn.click();
  }

  if (e.key === "ArrowLeft") {
    prevBtn.click();
  }
});
