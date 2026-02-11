const container = document.getElementById("solar3d");

const scene = new THREE.Scene();
scene.background = new THREE.Color(0xf5f7fb);

const camera = new THREE.PerspectiveCamera(
    45,
    container.clientWidth / container.clientHeight,
    0.1,
    1000
);
camera.position.set(0, 2, 6);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(container.clientWidth, container.clientHeight);
container.appendChild(renderer.domElement);

// LIGHT
const light = new THREE.DirectionalLight(0xffffff, 1);
light.position.set(5, 10, 7);
scene.add(light);

// SOLAR PANEL (BOX)
const geometry = new THREE.BoxGeometry(3, 0.1, 2);
const material = new THREE.MeshStandardMaterial({ color: 0x1e88e5 });
const panel = new THREE.Mesh(geometry, material);
scene.add(panel);

// ANIMATION
function animate() {
    requestAnimationFrame(animate);
    panel.rotation.y += 0.003;
    renderer.render(scene, camera);
}
animate();

// RESPONSIVE
window.addEventListener("resize", () => {
    camera.aspect = container.clientWidth / container.clientHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(container.clientWidth, container.clientHeight);
});
