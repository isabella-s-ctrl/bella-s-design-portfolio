// Verify JavaScript is connected
console.log('Portfolio site loaded successfully!');
console.log('Testing if JavaScript is working...');
console.log('Canvas test starting...');

// Aura Light Cursor Interaction (guard for pages without .hero)
document.addEventListener('DOMContentLoaded', function() {
    const hero = document.querySelector('.hero');
    if (!hero) return;
    const auraLights = document.querySelectorAll('.aura-light');
    let mouseX = 0;
    let mouseY = 0;
    let heroRect = hero.getBoundingClientRect();

    hero.addEventListener('mousemove', function(e) {
        mouseX = e.clientX - heroRect.left;
        mouseY = e.clientY - heroRect.top;
        auraLights.forEach((light) => {
            const lightRect = light.getBoundingClientRect();
            const lightX = lightRect.left - heroRect.left + lightRect.width / 2;
            const lightY = lightRect.top - heroRect.top + lightRect.height / 2;
            const distance = Math.sqrt((mouseX - lightX) ** 2 + (mouseY - lightY) ** 2);
            const pushRadius = 150;
            if (distance < pushRadius) {
                const pushX = (lightX - mouseX) / distance;
                const pushY = (lightY - mouseY) / distance;
                const pushStrength = (pushRadius - distance) / pushRadius;
                const maxPush = 50;
                const translateX = pushX * pushStrength * maxPush;
                const translateY = pushY * pushStrength * maxPush;
                light.style.transform += ` translate(${translateX}px, ${translateY}px)`;
                light.style.boxShadow = `0 0 40px rgba(91, 155, 213, 0.6), 0 0 80px rgba(91, 155, 213, 0.3)`;
            } else {
                light.style.boxShadow = `0 0 30px rgba(91, 155, 213, 0.4), 0 0 60px rgba(91, 155, 213, 0.2)`;
            }
        });
    });

    hero.addEventListener('mouseleave', function() {
        auraLights.forEach(light => {
            light.style.transform = '';
            light.style.boxShadow = `0 0 30px rgba(91, 155, 213, 0.4), 0 0 60px rgba(91, 155, 213, 0.2)`;
        });
    });

    window.addEventListener('resize', function() {
        heroRect = hero.getBoundingClientRect();
    });
});

// Word switching animation (only on home page)
const wordElement = document.getElementById('wordSwitcher');
if (wordElement) {
    const words = ['interfaces', 'visuals', 'events', 'brands'];
    let currentWordIndex = 0;

    function switchWord() {
        // Slide out and fade
        wordElement.style.transform = 'translateY(-20px)';
        wordElement.style.opacity = '0';
        
        setTimeout(() => {
            // Change word
            currentWordIndex = (currentWordIndex + 1) % words.length;
            wordElement.textContent = words[currentWordIndex];
            
            // Slide in and fade
            wordElement.style.transform = 'translateY(20px)';
            wordElement.style.opacity = '0';
            
            setTimeout(() => {
                wordElement.style.transform = 'translateY(0)';
                wordElement.style.opacity = '1';
            }, 50);
        }, 200);
    }

    // Start the word switching (faster - every 2 seconds)
    setInterval(switchWord, 2000);

    // Add smooth transition
    wordElement.style.transition = 'all 0.4s cubic-bezier(0.4, 0, 0.2, 1)';
}

// Smooth scrolling for navigation links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add active state to navigation links
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

window.addEventListener('scroll', () => {
    let current = '';
    sections.forEach(section => {
        const sectionTop = section.offsetTop;
        const sectionHeight = section.clientHeight;
        if (scrollY >= (sectionTop - 200)) {
            current = section.getAttribute('id');
        }
    });

    navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === `#${current}`) {
            link.classList.add('active');
        }
    });
});

// Form submission is now handled by FormSubmit - no JavaScript intervention needed

// Gallery filtering (only on gallery pages)
const filterButtons = document.querySelectorAll('.filter-btn');
const galleryItems = document.querySelectorAll('.gallery-item');

if (filterButtons.length > 0 && galleryItems.length > 0) {
    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');
            
            const filterValue = button.getAttribute('data-filter');
            
            galleryItems.forEach(item => {
                if (filterValue === 'all' || item.getAttribute('data-category') === filterValue) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeIn 0.5s ease';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
}

// Add fadeIn animation
const style = document.createElement('style');
style.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes cardShuffle {
        0% { opacity: 1; transform: translateY(0) scale(1); }
        50% { opacity: 0; transform: translateY(-20px) scale(0.95); }
        100% { opacity: 1; transform: translateY(0) scale(1); }
    }
`;
document.head.appendChild(style);

// Scroll progress bar (projects)
(() => {
    const bar = document.querySelector('.scroll-progress__bar');
    if (!bar) return;
    const getEl = () => document.scrollingElement || document.documentElement || document.body;
    const getScrollTop = () => getEl().scrollTop || 0;
    const getMaxScroll = () => {
        const el = getEl();
        return Math.max(0, (el.scrollHeight - el.clientHeight));
    };
    const update = () => {
        const top = getScrollTop();
        const max = getMaxScroll();
        const ratio = max > 0 ? Math.min(1, Math.max(0, top / max)) : 0;
        const pct = (ratio * 100);
        bar.style.width = pct + '%';
    };
    let ticking = false;
    window.addEventListener('scroll', () => {
        if (!ticking) {
            window.requestAnimationFrame(() => { update(); ticking = false; });
            ticking = true;
        }
    }, { passive: true });
    window.addEventListener('resize', update);
    document.addEventListener('visibilitychange', update);
    window.addEventListener('popstate', update);
    document.addEventListener('DOMContentLoaded', update);
    window.addEventListener('load', update);
    update();
    // Fallback: periodic update to catch any missed events
    setInterval(update, 200);
})();

// Quick Facts Shuffle Function (disabled - show all items statically)
function shuffleQuickFacts() {
    const factsGrid = document.querySelector('.facts-grid');
    if (!factsGrid) return;
    const factItems = Array.from(factsGrid.querySelectorAll('.fact-item'));
    factItems.forEach(item => {
        item.style.opacity = '1';
        item.style.transform = 'none';
        item.style.transition = 'none';
        item.style.display = 'block';
    });
}

// Disable shuffle timers to keep cards static
const factsGrid = document.querySelector('.facts-grid');
if (factsGrid) {
    // Ensure all are visible once on load
    document.addEventListener('DOMContentLoaded', shuffleQuickFacts);
    window.addEventListener('load', shuffleQuickFacts);
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded!');
    
    // Existing code...
    // Mark page as loaded to trigger section fade-ins
    document.documentElement.classList.add('page-loaded');

    // Scroll-triggered reveal (IntersectionObserver)
    const revealEls = document.querySelectorAll('.reveal-on-scroll');
    if (revealEls.length > 0 && 'IntersectionObserver' in window) {
        const io = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    io.unobserve(entry.target);
                }
            });
        }, { root: null, threshold: 0.15 });

        revealEls.forEach(el => io.observe(el));
    } else {
        // Fallback: show immediately if IO not supported
        revealEls.forEach(el => el.classList.add('revealed'));
    }

    // Floating Images Animation for Impact Section
    const impactSection = document.querySelector('.impact-section');
    if (impactSection && 'IntersectionObserver' in window) {
        const impactObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animate');
                    impactObserver.unobserve(entry.target);
                }
            });
        }, { root: null, threshold: 0.3 });

        impactObserver.observe(impactSection);
    }
}); 
// Lazy loading for optimized images (robust)
document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('img.optimized-image[loading="lazy"]');

    const ensureLoadedClass = (img) => {
        // If already loaded from cache, mark as loaded immediately
        if (img.complete && img.naturalWidth > 0) {
            img.classList.add('loaded');
            return true;
        }
        return false;
    };

    // Optional IO just to nudge browsers that are conservative with lazy assets
    let io = null;
    if ('IntersectionObserver' in window) {
        io = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    io.unobserve(entry.target);
                }
            });
        }, { rootMargin: '200px 0px', threshold: 0.01 });
    }

    images.forEach((img) => {
        // Add listeners once
        img.addEventListener('load', () => img.classList.add('loaded'), { once: true });
        img.addEventListener('error', () => img.classList.add('loaded'), { once: true });

        // If it is already complete (served from cache), mark loaded now
        if (!ensureLoadedClass(img) && io) {
            io.observe(img);
        }
    });
});

// FormSubmit success message handling
document.addEventListener('DOMContentLoaded', function() {
    // Check for success parameter in URL
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.get('success') === 'true') {
        // Show success message
        const successMessage = document.createElement('div');
        successMessage.innerHTML = `
            <div style="
                position: fixed;
                top: 20px;
                right: 20px;
                background: #4CAF50;
                color: white;
                padding: 15px 20px;
                border-radius: 8px;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                z-index: 1000;
                font-family: Arial, sans-serif;
                animation: slideIn 0.3s ease-out;
            ">
                ✓ Message sent successfully! I'll get back to you soon.
            </div>
            <style>
                @keyframes slideIn {
                    from { transform: translateX(100%); opacity: 0; }
                    to { transform: translateX(0); opacity: 1; }
                }
            </style>
        `;
        document.body.appendChild(successMessage);
        
        // Remove success message after 5 seconds
        setTimeout(() => {
            successMessage.remove();
            // Clean up URL
            const newUrl = window.location.href.split('?')[0];
            window.history.replaceState({}, document.title, newUrl);
        }, 5000);
    }
});
