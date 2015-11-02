

// caption.js 1.4
function Caption(element, picid, caption) {
  this.element = element;
  this.picid = picid;
  element.value = caption; // objects in Javascript are assigned by reference, so this works
  console.log('Caption .1, element: ' + element + ', picid: ' + picid + ', value: ' + caption);
  element.addEventListener("change", this, false); 
}

Caption.prototype.handleEvent = function(e) {
  if (e.type === "change") {
    console.log('handleEvent: caption changed!! value to ' + this.element.value )
    document.getElementById('caption').placeholder=this.element.value;
    this.update(this.element.value);
  }
}

Caption.prototype.change = function(value) {
  console.log('change: value: ' + value + ', this.data: ' + this.data +' -> ' + value + ', element.value: ' + this.element.value + ' -> ' + value )
  this.data = value;
  this.element.value = value;
}

Caption.prototype.update = function(caption) {
  makeCaptionPostRequest(this.picid, caption, function() {
    console.log('update: POST successful.');
  });
}


// caption.js 1.3
function makeCaptionPostRequest(picid, caption, cb) {
  var data = {
    'id': picid,
    'caption': caption
  };

  qwest.post('/225x7i1wcdi/pa3/pic/caption', data, {
    dataType: 'json',
    responseType: 'json'
  }).then(function(xhr, resp) {
    cb(resp);
  });
}


// caption.js 1.2
function makeCaptionRequest(picid, cb) {
    console.log('makeCaptionRequest .1.');
    qwest.get('/225x7i1wcdi/pa3/pic/caption?id=' + picid)
    .then(function(xhr, resp) {
      cb(resp);
    });
}


// 1.1
function initCaption(picid) {
    console.log('initCaption .1 . picid: ' + picid);
    var caption = document.getElementById("caption");
    console.log('initCaption .2 .');
    console.log(caption);
    var captionBinding = new Caption(caption, picid);

    makeCaptionRequest(picid, function(resp) {
        captionBinding.change(resp['caption']);
    });

    setInterval(function() {
        makeCaptionRequest(picid, function(resp) {
            captionBinding.change(resp['caption']);
        }); 
    }, 7000);
}