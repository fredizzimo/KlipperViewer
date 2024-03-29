/*
Viewer for Klipper toolpaths
Copyright (C) 2019  Fred Sundvik

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

var THREE = require('three');
var Plotly = require('plotly.js-dist');

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

var myRequest = new XMLHttpRequest();
myRequest.open("GET", "/plugin/KlipperViewer/get_data", true);
myRequest.onreadystatechange = function () { 
    if (myRequest.readyState === 4) {
        var response = JSON.parse(myRequest.responseText);
        var traces = [];
        var addTrace = function(axis) {
            var a = response[axis];
            var t = a.map(function(tuple) {
                return tuple[0]
            });
            var v= a.map(function(tuple) {
                return tuple[1]
            });
            traces.push({
                x: t,
                y: v,
            });
        }
        addTrace(1);
        addTrace(2);
        addTrace(3);

        var graph = document.getElementById("klipperviewer-graph");
        Plotly.plot(graph,
            traces,
            {
                //xaxis: {range: minMax},
                margin: { t: 0 }
            }
        );
        //document.getElementById("klipperresponse").innerHTML = myRequest.responseText;
    }
};
myRequest.send();
