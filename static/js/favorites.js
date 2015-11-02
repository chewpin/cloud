

// favorites.js 1.4
function LatestFavorite(element, picid, latest_favorite, favorite_count_value) {
  this.element = element;
  this.picid = picid;
  this.favorite_count_value = favorite_count_value;
  element.value = latest_favorite; // objects in Javascript are assigned by reference, so this works
  console.log('favorites .1, element: ' + element + ', picid: ' + picid + ', value: ' + latest_favorite + ", favorite_count_value: " + favorite_count_value);
}

LatestFavorite.prototype.change = function(value, value2) {
  console.log('LatestFavorite change: value: ' + value + ', this.data: ' + this.data +' -> ' + value + ', element.value: ' + this.element.value + ' -> ' + value + ",  value2: " + value2 )
  this.data = value;
  this.element.value = value;
  if ( this.element.value != null && this.element.value != "" ) {
    document.getElementById('favorite').innerHTML= value2 + " favorites, mostly recently favorited by " + this.element.value;
  }
}

// favorites.js 1.2
function makeLatestFavoriteRequest(picid, cb) {
    console.log('makeLatestFavoriteRequest .1. picid = ' + picid);
    qwest.get('/225x7i1wcdi/pa3/pic/favorites?id=' + picid)
    .then(function(xhr, resp) {
      cb(resp);
    });
}

function force_latest_favorite_update( picid ) {
  console.log('Force_latest_favorite_update .1 . picid: ' + picid);
  var latest_favorite = document.getElementById("favorite");
  console.log('Force_latest_favorite_update 2');
  // console.log('Force_latest_favorite_update .2 . ' + document.getElementById("latest_favorite").value);
  // var latest_favorite_value = document.getElementById("latest_favorite").value;
  // console.log('Force_latest_favorite_update .2 . ' + latest_favorite_value);
  // var favorite_count_value = document.getElementById("favorite_count").value;
  // console.log('initLatestFavorite .3 . favorite_count_value: ' + favorite_count_value);
  var latestFavoriteBinding = new LatestFavorite(latest_favorite, picid, null, null);

  makeLatestFavoriteRequest(picid, function(resp) {
      latestFavoriteBinding.change(resp['latest_favorite'], resp['num_favorites']);
  });
}

function initLatestFavorite(picid) {
    console.log('initLatestFavorite .1 . picid: ' + picid);
    var latest_favorite = document.getElementById("favorite");
    var latest_favorite_value = document.getElementById("latest_favorite").value;
    var favorite_count_value = document.getElementById("favorite_count").value;
    console.log('initLatestFavorite .2 . latest_favorite_value: ' + latest_favorite_value);
    console.log('initLatestFavorite .3 . favorite_count_value: ' + favorite_count_value);
    var latestFavoriteBinding = new LatestFavorite(latest_favorite, picid, latest_favorite_value, favorite_count_value);

    makeLatestFavoriteRequest(picid, function(resp) {
        latestFavoriteBinding.change(resp['latest_favorite'], resp['num_favorites']);
    });

    setInterval(function() {
        makeLatestFavoriteRequest(picid, function(resp) {
            latestFavoriteBinding.change(resp['latest_favorite'], resp['num_favorites']);
        }); 
    }, 10000);
}






function Like(element, picid, favorite_username) {
  this.element = element;
  this.picid = picid;
  this.favorite_username = favorite_username;
  element.value = favorite_username; // objects in Javascript are assigned by reference, so this works
  console.log('favorites .1, element: ' + element + ', picid: ' + picid + ', favorite_username: ' + favorite_username);
  element.addEventListener("click", this, false); 
}

Like.prototype.handleEvent = function(e) {
  if (e.type === "click") {
    console.log('handleEvent: favorites liked!! value to ' + this.element.value )
    this.update(this.element.value);

  }
}

Like.prototype.update = function(favorite_username) {
  var picid = this.picid;

  makeLikePostRequest(this.picid, this.favorite_username, function() {
    console.log('update: like POST successful.');
    console.log('NEED TO makeLatestFavoriteRequest picid = ' + picid)

    // makeLatestFavoriteRequest(picid, function(resp) {
    //     console.log('333 picid = ' + picid)
    //     latestFavoriteBinding.change(resp['latest_favorite']);
    // });
    force_latest_favorite_update(picid);
  });
}

function makeLikePostRequest(picid, favorite_username, cb) {
  var data = {
    'id': picid,
    'username': favorite_username
  };

  qwest.post('/225x7i1wcdi/pa3/pic/favorites', data, {
    dataType: 'json',
    responseType: 'json'
  }).then(function(xhr, resp) {
    cb(resp);
  });
}

// 1.1
function initLike(picid) {
    console.log('initLike .1 . picid: ' + picid);
    var like = document.getElementById("like");
    var favorite_username = document.getElementById("favorite_username").value;
    console.log('initLike .2 favorite_username: ' + favorite_username);
    var likeBinding = new Like(like, picid, favorite_username);
}





