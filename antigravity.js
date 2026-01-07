// Antigravity Effect - 修正版
// 修正: DOMContentLoadedを待ち、適切な初期化順序を実装

class AntigravityApp {
    constructor() {
        this.particles = [];
        this.mouseX = 0;
        this.mouseY = 0;
        this.container = null;
    }

    init() {
        // 修正1: thisをつけてcontainerプロパティに正しく代入
        this.container = document.getElementById('container');

        // 修正2: containerがnullの場合のエラーチェックを追加
        if (!this.container) {
            console.error('Container element not found!');
            return;
        }

        this.createParticles();
        this.addEventListeners();
        this.animate();
    }

    createParticles() {
        const particleCount = 50;

        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';

            const size = Math.random() * 20 + 10;
            particle.style.width = size + 'px';
            particle.style.height = size + 'px';

            const colors = ['#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24', '#6c5ce7'];
            particle.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];

            particle.style.left = Math.random() * window.innerWidth + 'px';
            particle.style.top = Math.random() * window.innerHeight + 'px';

            this.container.appendChild(particle);

            this.particles.push({
                element: particle,
                x: parseFloat(particle.style.left),
                y: parseFloat(particle.style.top),
                vx: (Math.random() - 0.5) * 2,
                vy: (Math.random() - 0.5) * 2,
                size: size
            });
        }
    }

    addEventListeners() {
        document.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX;
            this.mouseY = e.clientY;
        });
    }

    animate() {
        this.particles.forEach(particle => {
            const dx = this.mouseX - particle.x;
            const dy = this.mouseY - particle.y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 200) {
                const force = (200 - distance) / 200;
                particle.vx -= (dx / distance) * force * 0.5;
                particle.vy -= (dy / distance) * force * 0.5;
            }

            particle.vx *= 0.95;
            particle.vy *= 0.95;

            particle.x += particle.vx;
            particle.y += particle.vy;

            if (particle.x < 0) particle.x = window.innerWidth;
            if (particle.x > window.innerWidth) particle.x = 0;
            if (particle.y < 0) particle.y = window.innerHeight;
            if (particle.y > window.innerHeight) particle.y = 0;

            particle.element.style.left = particle.x + 'px';
            particle.element.style.top = particle.y + 'px';
        });

        requestAnimationFrame(() => this.animate());
    }
}

// 修正3: DOMContentLoadedイベントを待ってから初期化
document.addEventListener('DOMContentLoaded', () => {
    const app = new AntigravityApp();
    app.init();
});
