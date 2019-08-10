var THREE = require('three');

var container = document.getElementById("klipperviewer");
//document.body.appendChild( container );

var width = 200;
var height = 200;

var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera( 75, width / height, 0.1, 1000 );

//var renderer = new THREE.WebGLRenderer({canvas: container});
var renderer = new THREE.WebGLRenderer();
//renderer.setPixelRatio(window.devicePixelRatio);
renderer.setSize( width, height );
container.appendChild( renderer.domElement );

var geometry = new THREE.BoxGeometry( 1, 1, 1 );
var material = new THREE.MeshBasicMaterial( { color: 0x00ff00 } );
var cube = new THREE.Mesh( geometry, material );
scene.add( cube );

camera.position.z = 5;

function animate() {
    requestAnimationFrame( animate );
    cube.rotation.x += 0.01;
    cube.rotation.y += 0.01;
	renderer.render( scene, camera );
}
animate();