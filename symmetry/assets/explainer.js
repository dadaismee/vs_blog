const size = 30; // size of circle
let pix = []; 
let cols, rows;
let blockSize = 15; // size of 'pixel'
let imgSource = "assets/dog.png"
let canvas;
let oldBlockSize = 15;

function preload() {
  img = loadImage(imgSource);
}

function setup() {
  container = document.getElementById('p5-container');
  let w = container.clientWidth;
  let h = container.clientHeight;
  canvas = createCanvas(w, h);
  colorMode(RGB);
  textAlign(CENTER);
  img.resize(300, 0);
  canvas.parent('p5-container');
}

function draw() {
  background(255);
  let depth = parseInt(document.getElementById('p5-slider').value);

  const x = width / 4;
  const y = height/2;

  push();
    translate(x, y);
    fill(random(), 0, 0)
    drawCircles(0, 0, size / 1.75, depth);
    fill(0, 0, 0);
    noStroke()
    ellipse(0, 0, size, size);
    if (depth == 0) {
      fill(0, 0, 0);
      text('Понятие', 0, 30)
    }
  pop();

  blockSize = map(depth, 0, 3, 15, 1);

  push();
  translate(width/2, height/2 - img.height/2);
  noStroke();
  if (blockSize !== 1) {
    cols = width/blockSize;
    rows = height/blockSize;

    for (i=0; i < cols; i++) {
      pix[i] = [];
      for (j=0; j < rows; j++) {
        let x = i*blockSize;
        let y = j*blockSize;
        pix[i][j] = img.get(x, y);
        fill(pix[i][j])
        rect(x, y, blockSize, blockSize)
      }
    }
  } else {
    image(img, 0, 0);
  }
  pop();
}

function drawCircles(x, y, size, iteration) {
  if (iteration === 0) {
    return;
  }

  let circles = 6 // map(mouseX, 0, windowWidth, 1, 4)
  const angleStep = 360 / circles;
  const radius = size * 2;

  for (let angle = 0; angle < 360; angle += angleStep) {
    let newX = x + cos(radians(angle)) * radius;
    let newY = y + sin(radians(angle)) * radius;
    line(newX, newY, x, y);
    fill(angle, angle, angle)
    drawCircles(newX, newY, size, iteration - 1);
    ellipse(newX, newY, size, size);
  }
}

document.getElementById('p5-slider').addEventListener('input', () => {
  redraw();
});

// const size = 30; // size of circle
// let pix = []; 
// let cols, rows;
// let blockSize = 15; // size of 'pixel'
// let imgSource = "assets/dog.png"
// let canvas;
//
// function preload() {
//   img = loadImage(imgSource);
// }
//
// function setup() {
//    container = document.getElementById('p5-container');
//   let w = container.clientWidth;
//   let h = container.clientHeight;
//   canvas = createCanvas(w, h);
//   colorMode(RGB);
//   textAlign(CENTER);
//   img.resize(300, 0);
//   canvas.parent('p5-container');
// }
//
// function draw() {
//   let depth = parseInt(document.getElementById('p5-slider').value);
//
//   const x = width / 4;
//   const y = height/2;
//
//   background(255);
//   push();
//     translate(x, y);
//     fill(random(), 0, 0)
//     drawCircles(0, 0, size / 1.75, depth);
//     ellipse(0, 0, size, size);
//     text('Понятие', 0, 30)
//   pop();
//
//   blockSize = map(depth, 0, 2, 15, 1);
//   push();
//     translate(width/2, height/2 - img.height/2);
//     cols = width/blockSize;
//     rows = height/blockSize;
//
//     for (i=0; i < cols; i++) {
//       pix[i] = [];
//       for (j=0; j < rows; j++) {
//         let x = i*blockSize;
//         let y = j*blockSize;
//         pix[i][j] = img.get(x, y);
//       }
//     }
//
//     noStroke();
//     for (i=0; i < cols; i++) {
//       for (j=0; j < rows; j++) {
//         let x = i*blockSize;
//         let y = j*blockSize;
//         fill(pix[i][j])
//         rect(x, y, blockSize, blockSize)
//       }
//     }
//   pop();
// }
//
// function drawCircles(x, y, size, iteration) {
//   if (iteration === 0) {
//     return;
//   }
//
//   let circles = 6 // map(mouseX, 0, windowWidth, 1, 4)
//   const angleStep = 360 / circles;
//   const radius = size * 3;
//
//   for (let angle = 0; angle < 360; angle += angleStep) {
//     let newX = x + cos(radians(angle)) * radius;
//     let newY = y + sin(radians(angle)) * radius;
//     line(newX, newY, x, y);
//     fill(angle, angle, angle)
//     drawCircles(newX, newY, size, iteration - 1);
//     ellipse(newX, newY, size, size);
//   }
// }
//
// document.getElementById('p5-slider').addEventListener('input', () => {
//   redraw();
// });
