document.addEventListener('DOMContentLoaded', () => {
    VANTA.FOG({
        el: "#vanta-bg", // The background element
        highlightColor: 0xffc300, // Yellow highlight
        midtoneColor: 0xff1f00, // Red midtone
        lowlightColor: 0x2d00ff, // Blue lowlight
        baseColor: 0xffebeb, // Light pink base
        blurFactor: 0.6, // Set blur factor
        zoom: 1.0, // Default zoom level
        speed: 1.0, // Default speed
        mouseControls: true,
        touchControls: true,
        gyroControls: false,
        minHeight: 200.00,
        minWidth: 200.00
    });
});