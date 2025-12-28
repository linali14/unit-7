import React, { useEffect, useRef } from 'react';
import * as THREE from 'three';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

/**
 * Unit 7 Programming Assignment: 3D Function Grapher
 * * Objectives:
 * 1. Plot z = f(x,y) = x² - y² for x, y in [-1, 1] with 0.1 increments.
 * 2. Implement mouse controls (OrbitControls) for rotation and scaling.
 * 3. Include Axis Helper and Ground Plane.
 */
const FunctionGrapher = () => {
  const mountRef = useRef(null);

  useEffect(() => {
    // --- 1. INITIALIZATION ---
    const scene = new THREE.Scene();
    scene.background = new THREE.Color(0x111111);

    const camera = new THREE.PerspectiveCamera(
      45,
      window.innerWidth / window.innerHeight,
      0.1,
      1000
    );
    camera.position.set(3, 3, 3);

    const renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setPixelRatio(window.devicePixelRatio);
    mountRef.current.appendChild(renderer.domElement);

    // --- 2. CONTROLS ---
    const controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;

    // --- 3. HELPERS ---
    const axesHelper = new THREE.AxesHelper(2);
    scene.add(axesHelper);

    // Ground plane at y=0
    const gridHelper = new THREE.GridHelper(4, 20, 0x444444, 0x222222);
    scene.add(gridHelper);

    // --- 4. LIGHTING ---
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0xffffff, 1);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    // --- 5. FUNCTION PLOTTING (z = x² - y²) ---
    // Note: In Three.js coordinates, we map result 'z' to the Y axis.
    const f = (x, z) => (x * x) - (z * z);

    const generateGraph = () => {
      const geometry = new THREE.BufferGeometry();
      const vertices = [];
      const colors = [];
      const indices = [];

      const min = -1;
      const max = 1;
      const step = 0.1;
      const segments = Math.round((max - min) / step);

      // Color Palette: Highs (Red) and Lows (Blue)
      const colorHigh = new THREE.Color(0xd43333); 
      const colorLow = new THREE.Color(0x1e66ff);

      for (let i = 0; i <= segments; i++) {
        const x = min + (i * step);
        for (let j = 0; j <= segments; j++) {
          const z = min + (j * step);
          const y = f(x, z);

          vertices.push(x, y, z);

          // Normalize Y for color (Range is roughly -1 to 1)
          const normalizedY = (y + 1) / 2;
          const vertexColor = new THREE.Color().copy(colorLow).lerp(colorHigh, THREE.MathUtils.clamp(normalizedY, 0, 1));
          colors.push(vertexColor.r, vertexColor.g, vertexColor.b);
        }
      }

      for (let i = 0; i < segments; i++) {
        for (let j = 0; j < segments; j++) {
          const a = i * (segments + 1) + j;
          const b = (i + 1) * (segments + 1) + j;
          const c = (i + 1) * (segments + 1) + (j + 1);
          const d = i * (segments + 1) + (j + 1);

          indices.push(a, b, d);
          indices.push(b, c, d);
        }
      }

      geometry.setIndex(indices);
      geometry.setAttribute('position', new THREE.Float32BufferAttribute(vertices, 3));
      geometry.setAttribute('color', new THREE.Float32BufferAttribute(colors, 3));
      geometry.computeVertexNormals();

      const material = new THREE.MeshPhongMaterial({
        vertexColors: true,
        side: THREE.DoubleSide,
        shininess: 60,
        transparent: true,
        opacity: 0.9
      });

      const mesh = new THREE.Mesh(geometry, material);
      
      // Wireframe for structural clarity
      const wireframe = new THREE.LineSegments(
        new THREE.WireframeGeometry(geometry),
        new THREE.LineBasicMaterial({ color: 0xffffff, transparent: true, opacity: 0.2 })
      );
      mesh.add(wireframe);

      scene.add(mesh);
    };

    generateGraph();

    // --- 6. RENDER LOOP ---
    const animate = () => {
      requestAnimationFrame(animate);
      controls.update();
      renderer.render(scene, camera);
    };

    const handleResize = () => {
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    };

    window.addEventListener('resize', handleResize);
    animate();

    return () => {
      window.removeEventListener('resize', handleResize);
      if (mountRef.current && renderer.domElement) {
        mountRef.current.removeChild(renderer.domElement);
      }
    };
  }, []);

  return (
    <div style={{ width: '100%', height: '100vh', position: 'relative' }}>
      <div style={{
        position: 'absolute',
        top: '20px',
        left: '20px',
        padding: '10px 15px',
        background: 'rgba(0,0,0,0.8)',
        color: '#fff',
        borderRadius: '4px',
        fontFamily: 'sans-serif',
        zIndex: 5,
        borderLeft: '4px solid #2dbd5a'
      }}>
        <h3 style={{ margin: 0 }}>Saddle Surface</h3>
        <p style={{ margin: '5px 0 0 0', fontSize: '14px' }}>z = x² - y²</p>
      </div>
      <div ref={mountRef} style={{ width: '100%', height: '100%' }} />
    </div>
  );
};

export default function App() {
  return <FunctionGrapher />;
}
