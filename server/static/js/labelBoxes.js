function labelBoxes (name) {
    const id2label = {0: 'O', 1: 'HEADER', 2: 'QUESTION', 3: 'ANSWER'}
    // const id2label = {0: 'O', 1: 'B-HEADER', 2: 'I-HEADER', 3: 'B-QUESTION', 4: 'I-QUESTION', 5: 'B-ANSWER', 6: 'I-ANSWER'}
    const id2color = ["violet", "orange", "blue", "green"]
    // const id2color = ["violet", "orange", "orange", "blue", "blue", "green", "green"]
    
    const canva = document.getElementById("Preview")
    const ctx = canva.getContext("2d");
    const img = new Image();
    
    img.src = "/uploads/" + name
    img.addEventListener("load", () => {
      canva.width = img.width;
      canva.height = img.height;
      ctx.drawImage(img, 0, 0);
    });
    fetch("/process/" + name).then(res => res.json().then(j => {
      // ctx.strokeStyle = "red"
      // for (var i = 0; i < j["ocr_boxes"].length; i++){
      //   const bbox = j["ocr_boxes"][i]
      //   let box = [...bbox[0], ...bbox[2]];
      //   box[3] = box[3] - box[1];
      //   box[2] = box[2] - box[0];
      //   ctx .strokeRect(...box);
      // }
    
      for (var i = 0; i < j["boxes"].length; i++){
        const bbox = j["boxes"][i]
        let box = [...bbox[0], ...bbox[2]];
        box[3] = box[3] - box[1];
        box[2] = box[2] - box[0];
        console.log(j["pred"][i])
        console.log(box)
        ctx.lineWidth = 10;
        ctx.strokeStyle = id2color[j["pred"][i]]
        ctx .strokeRect(...box);
      }
    
      ctx.strokeStyle = "black"
      for (var i = 0; i < j["links"].length; i++){
        const link = j["links"][i]
        console.log(link);
        let box = link[0];
        // box[3] = box[3] - box[1];
        // box[2] = box[2] - box[0];
        ctx.moveTo(...box[1]);
        box = link[1]
        ctx.lineTo(...box[0]);
        ctx .stroke();
      }
    }))
}

function hidelabel () {
  const canva = document.getElementById("Preview")
  const ctx = canva.getContext("2d");
  ctx.clearRect(0,0,canva.width, canva.height)
}