import * as THREE from 'https://cdn.skypack.dev/three@0.130.0/build/three.module.js';
import { STLLoader } from 'https://cdn.skypack.dev/three@0.130.0/examples/jsm/loaders/STLLoader.js';
import { OrbitControls } from 'https://cdn.skypack.dev/three@0.130.0/examples/jsm/controls/OrbitControls.js'

const windowdocument = window.document
const scriptelement = windowdocument.getElementById("javascript");
const name = scriptelement.getAttribute("name");
const filename = scriptelement.getAttribute("filename");

const scene = new THREE.Scene();
scene.background = new THREE.Color( 0xffffff );
const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

const renderer = new THREE.WebGLRenderer();
renderer.setSize( window.innerWidth/2, window.innerHeight/2 );
/*document.body.appendChild( renderer.domElement );*/
document.getElementById("javascript").insertAdjacentElement("afterend", renderer.domElement);

const material = new THREE.MeshPhysicalMaterial({
    color: 0x1f77b4,
    metalness: 0.4,
    roughness: 0.1,
    opacity: 1.0,
    transparent: true,
    transmission: 0.99,
    clearcoat: 0.0,
    clearcoatRoughness: 0.25,
    side: THREE.DoubleSide
})

const loader = new STLLoader()
loader.load(
    '/static/stls/' + name + '_' + filename + '.stl',
    function (geometry) {
        const mesh = new THREE.Mesh(geometry, material)
        scene.add(mesh)
        mesh.scale.set(0.2,0.2,0.2)
        mesh.rotation.set(-Math.PI/2,0,0)
        mesh.traverse( function ( child ) { /*from https://stackoverflow.com/questions/40963990/three-js-load-an-obj-translate-to-origin-center-in-scene-orbit*/

            if ( child instanceof THREE.Mesh ) {

               child.material = material;
               child.geometry.center();
            }
        })
    },
    (xhr) => {
        console.log((xhr.loaded / xhr.total) * 100 + '% loaded')
    },
    (error) => {
        console.log(error)
    }
)

const intensity = 40;
const light = new THREE.DirectionalLight(0xffffff, intensity);
light.position.set(-1, 4, 4);
scene.add(light);

const orbit = new OrbitControls(camera, renderer.domElement);
orbit.enableDamping = true;

camera.position.z = 5;
camera.position.y = 2.9;
orbit.update()

function animate() {
    requestAnimationFrame( animate );
    orbit.update();
    renderer.render( scene, camera );
};

animate();

window.addEventListener('resize', function() {
    camera.aspect = window.innerWidth / this.window.innherHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
})