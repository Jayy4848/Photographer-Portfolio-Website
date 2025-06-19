/**
 * 3D CINEMATIC PHOTOGRAPHY PORTFOLIO
 * Main JavaScript File
 * ===================================
 */

// Global Variables
let isLoading = true;
let navbar, backToTopBtn, loadingScreen;
let scroll, lightbox;

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

// Initialize the application
function initializeApp() {
    // Cache DOM elements
    navbar = document.getElementById('mainNav');
    backToTopBtn = document.getElementById('backToTop');
    loadingScreen = document.getElementById('loading-screen');
    
    // Initialize components
    initializeLoading();
    initializeNavigation();
    initializeScrollEffects();
    initializeAnimations();
    initializeParticles();
    initializeFormHandlers();
    initializeLazyLoading();
    
    // Initialize lightbox after a short delay to ensure all elements are loaded
    setTimeout(() => {
        initializeLightbox();
    }, 500);
    
    // Initialize page-specific functionality
    if (document.body.classList.contains('home-page')) {
        initializeHomePage();
    }
    
    console.log('🎉 Photography Portfolio Initialized Successfully!');
}

// ===== LOADING SCREEN =====
function initializeLoading() {
    if (!loadingScreen) return;
    
    // Simulate loading progress
    const progressBar = loadingScreen.querySelector('.loading-progress');
    let progress = 0;
    
    const interval = setInterval(() => {
        progress += Math.random() * 30;
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            
            // Hide loading screen after a short delay
            setTimeout(() => {
                loadingScreen.classList.add('hidden');
                isLoading = false;
                
                // Initialize AOS after loading
                if (typeof AOS !== 'undefined') {
                    AOS.init({
                        duration: 1000,
                        offset: 100,
                        once: true,
                        easing: 'ease-out-cubic'
                    });
                }
                
                // Start entrance animations
                startEntranceAnimations();
            }, 500);
        }
        
        if (progressBar) {
            progressBar.style.width = progress + '%';
        }
    }, 100);
}

// ===== NAVIGATION EFFECTS =====
function initializeNavigation() {
    if (!navbar) return;
    
    // Navbar scroll effect
    let lastScrollTop = 0;
    
    window.addEventListener('scroll', () => {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Add scrolled class when not at top
        if (scrollTop > 100) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
        
        // Hide/show navbar on scroll
        if (scrollTop > lastScrollTop && scrollTop > 500) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
    });
    
    // Active nav link highlighting
    const navLinks = navbar.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');
    
    if (sections.length > 0) {
        window.addEventListener('scroll', () => {
            let current = '';
            
            sections.forEach(section => {
                const sectionTop = section.offsetTop;
                const sectionHeight = section.clientHeight;
                if (pageYOffset >= sectionTop - 200) {
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
    }
}

// ===== SCROLL EFFECTS =====
function initializeScrollEffects() {
    // Back to top button
    if (backToTopBtn) {
        window.addEventListener('scroll', () => {
            if (window.pageYOffset > 300) {
                backToTopBtn.classList.add('show');
            } else {
                backToTopBtn.classList.remove('show');
            }
        });
        
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }
    
    // Parallax effects for background elements
    const parallaxElements = document.querySelectorAll('[data-parallax]');
    
    if (parallaxElements.length > 0) {
        window.addEventListener('scroll', () => {
            parallaxElements.forEach(element => {
                const speed = element.getAttribute('data-parallax') || 0.5;
                const yPos = -(window.pageYOffset * speed);
                element.style.transform = `translateY(${yPos}px)`;
            });
        });
    }
    
    // Smooth scrolling for anchor links
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
}

// ===== LIGHTBOX INITIALIZATION =====
function initializeLightbox() {
    console.log('Initializing GLightbox...');
    if (typeof GLightbox !== 'undefined') {
        console.log('GLightbox available, creating instance...');
        // Store globally for reinitializing from other pages
        window.lightbox = GLightbox({
            selector: '.gallery-item a, [data-gallery], .gallery-lightbox, [data-glightbox]',
            touchNavigation: true,
            loop: true,
            autoplayVideos: false,
            closeOnOutsideClick: true,
            escKey: true,
            keyboardNavigation: true,
            preload: true,
            openEffect: 'fade',
            closeEffect: 'fade',
            slideEffect: 'slide',
            moreText: 'See more',
            moreLength: 60,
            descPosition: 'bottom',
            height: '90vh',
            width: '90vw',
            cssEfects: {
                fade: { in: 'fadeIn', out: 'fadeOut' },
                zoom: { in: 'zoomIn', out: 'zoomOut' }
            },
            svg: {
                close: '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>',
                next: '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="9,18 15,12 9,6"></polyline></svg>',
                prev: '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polyline points="15,18 9,12 15,6"></polyline></svg>'
            },
            plyr: {
                config: {
                    ratio: '16:9',
                    youtube: {
                        noCookie: true,
                        rel: 0,
                        showinfo: 0,
                        iv_load_policy: 3
                    }
                }
            },
            onOpen: function() {
                console.log('Lightbox opened');
                
                // Force create close button if it doesn't exist
                setTimeout(() => {
                    let closeBtn = document.querySelector('.gclose, .glightbox-close');
                    
                    if (!closeBtn) {
                        console.log('No close button found, creating one...');
                        closeBtn = document.createElement('button');
                        closeBtn.className = 'gclose custom-close-btn';
                        closeBtn.innerHTML = '×';
                        closeBtn.setAttribute('aria-label', 'Close');
                        document.body.appendChild(closeBtn);
                        
                        closeBtn.addEventListener('click', function() {
                            if (window.lightbox) {
                                window.lightbox.close();
                            }
                        });
                    }
                    
                    // Apply aggressive styling
                    if (closeBtn) {
                        console.log('Styling close button...');
                        closeBtn.style.cssText = `
                            background: rgba(255, 0, 0, 0.9) !important;
                            border-radius: 50% !important;
                            padding: 15px !important;
                            width: 60px !important;
                            height: 60px !important;
                            display: flex !important;
                            align-items: center !important;
                            justify-content: center !important;
                            position: fixed !important;
                            top: 20px !important;
                            right: 20px !important;
                            z-index: 999999 !important;
                            border: 3px solid rgba(255, 255, 255, 0.8) !important;
                            color: white !important;
                            font-size: 36px !important;
                            font-weight: bold !important;
                            cursor: pointer !important;
                            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.5) !important;
                            visibility: visible !important;
                            opacity: 1 !important;
                            transition: all 0.3s ease !important;
                        `;
                        
                        closeBtn.addEventListener('mouseenter', function() {
                            this.style.background = 'rgba(255, 255, 255, 0.95) !important';
                            this.style.color = '#000 !important';
                            this.style.transform = 'scale(1.2) !important';
                            this.style.borderColor = 'rgba(255, 0, 0, 0.8) !important';
                        });
                        
                        closeBtn.addEventListener('mouseleave', function() {
                            this.style.background = 'rgba(255, 0, 0, 0.9) !important';
                            this.style.color = 'white !important';
                            this.style.transform = 'scale(1) !important';
                            this.style.borderColor = 'rgba(255, 255, 255, 0.8) !important';
                        });
                    }
                    
                    // Add instruction text
                    const container = document.querySelector('.gcontainer, body');
                    if (container && !document.querySelector('.lightbox-instructions')) {
                        const instructions = document.createElement('div');
                        instructions.className = 'lightbox-instructions';
                        instructions.innerHTML = `
                            <div style="
                                position: fixed;
                                top: 90px;
                                right: 20px;
                                background: rgba(0, 0, 0, 0.8);
                                color: white;
                                padding: 12px 18px;
                                border-radius: 8px;
                                font-size: 14px;
                                z-index: 999998;
                                animation: fadeInOut 5s ease-in-out;
                                box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
                            ">
                                Click RED X button or press ESC to close
                            </div>
                        `;
                        container.appendChild(instructions);
                        
                        // Remove after 5 seconds
                        setTimeout(() => {
                            if (instructions && instructions.parentNode) {
                                instructions.parentNode.removeChild(instructions);
                            }
                        }, 5000);
                    }
                }, 100);
            },
            onClose: function() {
                console.log('Lightbox closed');
                // Remove custom close button if it exists
                const customCloseBtn = document.querySelector('.custom-close-btn');
                if (customCloseBtn && customCloseBtn.parentNode) {
                    customCloseBtn.parentNode.removeChild(customCloseBtn);
                }
            },
            beforeSlideChange: (slide, data) => {
                console.log('Slide changing', slide, data);
            }
        });
        console.log('GLightbox initialized successfully');
        console.log('Lightbox instance:', window.lightbox);
        
        // Debug: Check how many elements are found
        const elements = document.querySelectorAll('.gallery-item a, [data-gallery], .gallery-lightbox, [data-glightbox]');
        console.log(`Found ${elements.length} lightbox elements:`, elements);
        
        // Make reinitialize function globally available
        window.reinitializeLightbox = function() {
            console.log('Reinitializing lightbox...');
            if (window.lightbox) {
                window.lightbox.destroy();
            }
            initializeLightbox();
        };
        
    } else {
        console.error('GLightbox not available!');
    }
}

// Add function to refresh lightbox when new content is loaded
function refreshLightbox() {
    console.log('Refreshing lightbox...');
    if (window.lightbox && typeof window.lightbox.reload === 'function') {
        window.lightbox.reload();
    } else if (window.reinitializeLightbox) {
        window.reinitializeLightbox();
    }
}

// ===== ANIMATIONS =====
function initializeAnimations() {
    // Register GSAP plugins
    if (typeof gsap !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
        
        // Set up timeline for page transitions
        const tl = gsap.timeline();
        
        // Fade in page content
        gsap.set('main', { opacity: 0, y: 30 });
        
        // Animate cards on scroll
        gsap.utils.toArray('.card, .gallery-item').forEach(card => {
            gsap.fromTo(card, 
                { y: 60, opacity: 0 },
                {
                    y: 0,
                    opacity: 1,
                    duration: 0.8,
                    ease: 'power3.out',
                    scrollTrigger: {
                        trigger: card,
                        start: 'top 85%',
                        end: 'bottom 15%',
                        toggleActions: 'play none none reverse'
                    }
                }
            );
        });
        
        // Animate text elements
        gsap.utils.toArray('.display-1, .display-2, .display-3, .display-4, .display-5').forEach(title => {
            gsap.fromTo(title.children || title,
                { y: 100, opacity: 0 },
                {
                    y: 0,
                    opacity: 1,
                    duration: 1,
                    ease: 'power3.out',
                    stagger: 0.1,
                    scrollTrigger: {
                        trigger: title,
                        start: 'top 85%'
                    }
                }
            );
        });
        
        // Floating animations for images
        gsap.utils.toArray('.float').forEach(element => {
            gsap.to(element, {
                y: -20,
                duration: 3,
                ease: 'power2.inOut',
                repeat: -1,
                yoyo: true
            });
        });
    }
}

// ===== ENTRANCE ANIMATIONS =====
function startEntranceAnimations() {
    if (typeof gsap !== 'undefined') {
        const tl = gsap.timeline();
        
        tl.to('main', { 
            opacity: 1, 
            y: 0, 
            duration: 1, 
            ease: 'power3.out' 
        });
        
        // Animate hero content if on home page
        if (document.querySelector('.hero-content')) {
            tl.from('.hero-title', { 
                y: 100, 
                opacity: 0, 
                duration: 1, 
                ease: 'power3.out' 
            }, '-=0.5')
            .from('.hero-subtitle', { 
                y: 50, 
                opacity: 0, 
                duration: 0.8, 
                ease: 'power3.out' 
            }, '-=0.3')
            .from('.hero-cta', { 
                y: 30, 
                opacity: 0, 
                duration: 0.6, 
                ease: 'power3.out' 
            }, '-=0.2');
        }
    }
}

// ===== PARTICLE SYSTEM =====
function initializeParticles() {
    const particleContainer = document.querySelector('.particles-container');
    if (!particleContainer) return;
    
    // Create floating particles
    for (let i = 0; i < 50; i++) {
        createParticle(particleContainer);
    }
}

function createParticle(container) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.cssText = `
        position: absolute;
        width: 4px;
        height: 4px;
        background: rgba(255, 255, 255, 0.5);
        border-radius: 50%;
        pointer-events: none;
        animation: float-particle ${Math.random() * 10 + 5}s infinite linear;
        left: ${Math.random() * 100}%;
        animation-delay: ${Math.random() * 5}s;
    `;
    
    container.appendChild(particle);
}

// ===== FORM HANDLERS =====
function initializeFormHandlers() {
    // Contact form
    const contactForm = document.querySelector('.contact-form');
    if (contactForm) {
        contactForm.addEventListener('submit', handleFormSubmission);
    }
    
    // Newsletter form
    const newsletterForms = document.querySelectorAll('.newsletter-form');
    newsletterForms.forEach(form => {
        form.addEventListener('submit', handleNewsletterSubmission);
    });
    
    // Form field animations
    const formFields = document.querySelectorAll('.form-control');
    formFields.forEach(field => {
        field.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        field.addEventListener('blur', function() {
            if (!this.value) {
                this.parentElement.classList.remove('focused');
            }
        });
    });
    
    // Initialize quick action buttons
    initializeQuickActionButtons();
}

// Quick action buttons functionality
function initializeQuickActionButtons() {
    // Call button functionality
    const callButtons = document.querySelectorAll('a[href^="tel:"], .btn[href^="tel:"]');
    callButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const phoneNumber = this.getAttribute('href').replace('tel:', '');
            showNotification(`Calling ${phoneNumber}...`, 'info');
            
            // For mobile devices, the tel: link will work automatically
            // For desktop, show a notification
            if (!isMobile) {
                e.preventDefault();
                showNotification(`Please call ${phoneNumber} from your mobile device`, 'info');
            }
        });
    });
    
    // WhatsApp button functionality
    const whatsappButtons = document.querySelectorAll('a[href*="wa.me"], .btn[href*="wa.me"]');
    whatsappButtons.forEach(button => {
        button.addEventListener('click', function() {
            showNotification('Opening WhatsApp...', 'success');
        });
    });
    
    // Email button functionality
    const emailButtons = document.querySelectorAll('a[href^="mailto:"], .btn[href^="mailto:"]');
    emailButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const email = this.getAttribute('href').replace('mailto:', '');
            showNotification(`Opening email client to send message to ${email}...`, 'info');
            
            // For better UX on some devices
            setTimeout(() => {
                if (!isMobile) {
                    showNotification('If your email client didn\'t open, please send an email manually', 'info');
                }
            }, 2000);
        });
    });
}

// Handle form submission
async function handleFormSubmission(e) {
    e.preventDefault();
    
    const form = e.target;
    const formData = new FormData(form);
    const submitBtn = form.querySelector('button[type="submit"], input[type="submit"]');
    
    // Validate required fields
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    if (!isValid) {
        showNotification('Please fill in all required fields.', 'error');
        return;
    }
    
    // Show loading state
    const originalText = submitBtn.textContent || submitBtn.value;
    if (submitBtn.textContent) {
        submitBtn.textContent = 'Sending...';
    } else {
        submitBtn.value = 'Sending...';
    }
    submitBtn.disabled = true;
    
    try {
        const response = await fetch(form.action || window.location.href, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
            }
        });
        
        if (response.headers.get('content-type')?.includes('application/json')) {
            const data = await response.json();
            
            if (data.success) {
                showNotification(data.message || 'Message sent successfully! We\'ll get back to you soon.', 'success');
                form.reset();
                
                // Remove any error styling
                form.querySelectorAll('.is-invalid').forEach(field => {
                    field.classList.remove('is-invalid');
                });
            } else {
                showNotification('Please correct the errors and try again.', 'error');
                
                // Show field-specific errors if available
                if (data.errors) {
                    Object.keys(data.errors).forEach(fieldName => {
                        const field = form.querySelector(`[name="${fieldName}"]`);
                        if (field) {
                            field.classList.add('is-invalid');
                        }
                    });
                }
            }
        } else {
            // Handle regular form submission (non-AJAX)
            if (response.ok) {
                showNotification('Message sent successfully! We\'ll get back to you soon.', 'success');
                form.reset();
            } else {
                showNotification('There was an error sending your message. Please try again.', 'error');
            }
        }
    } catch (error) {
        console.error('Form submission error:', error);
        showNotification('An error occurred. Please try again or contact us directly.', 'error');
    } finally {
        if (submitBtn.textContent) {
            submitBtn.textContent = originalText;
        } else {
            submitBtn.value = originalText;
        }
        submitBtn.disabled = false;
    }
}

// Handle newsletter submission
async function handleNewsletterSubmission(e) {
    e.preventDefault();
    
    const form = e.target;
    const email = form.querySelector('input[type="email"]').value;
    
    if (!email) {
        showNotification('Please enter a valid email address.', 'error');
        return;
    }
    
    // Simulate newsletter subscription
    showNotification('Thank you for subscribing!', 'success');
    form.reset();
}

// ===== LAZY LOADING =====
function initializeLazyLoading() {
    const lazyImages = document.querySelectorAll('img[data-src]');
    
    if ('IntersectionObserver' in window) {
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });
        
        lazyImages.forEach(img => imageObserver.observe(img));
    } else {
        // Fallback for older browsers
        lazyImages.forEach(img => {
            img.src = img.dataset.src;
            img.classList.remove('lazy');
        });
    }
}

// ===== HOME PAGE SPECIFIC =====
function initializeHomePage() {
    initializeHeroEffects();
    initializeStatsCounters();
    initializeTestimonialSlider();
    initializeGalleryEffects();
}

// Hero section effects
function initializeHeroEffects() {
    const heroSection = document.querySelector('.hero-section');
    if (!heroSection) return;
    
    // Initialize smooth seasonal video rotation
    initializeSeasonalVideos();
    
    // Parallax effect for hero background
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const parallax = heroSection.querySelector('.hero-bg');
        if (parallax) {
            parallax.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
    
    // Typing effect for hero title
    const heroTitle = document.querySelector('.hero-title');
    if (heroTitle && typeof gsap !== 'undefined') {
        const text = heroTitle.textContent;
        heroTitle.textContent = '';
        
        gsap.to(heroTitle, {
            duration: 2,
            text: text,
            ease: 'none',
            delay: 1
        });
    }
}

// Smooth seasonal video rotation
function initializeSeasonalVideos() {
    const videos = document.querySelectorAll('.seasonal-video');
    if (videos.length === 0) return;
    
    let currentVideoIndex = 0;
    const seasons = ['MONSOON', 'SUMMER', 'WINTER'];
    
    // Ensure all videos are properly loaded
    videos.forEach((video, index) => {
        video.load(); // Preload videos
        video.muted = true;
        video.loop = true;
        video.playsInline = true;
        
        // Set initial state
        if (index === 0) {
            video.style.opacity = '1';
            video.classList.add('active');
            video.play().catch(e => console.log('Video autoplay failed:', e));
        } else {
            video.style.opacity = '0';
            video.classList.remove('active');
        }
        
        // Handle video loading errors
        video.addEventListener('error', function() {
            console.log(`Video ${index} failed to load, showing fallback image`);
            this.style.display = 'none';
            const fallbackImg = this.querySelector('img');
            if (fallbackImg) {
                fallbackImg.style.display = 'block';
            }
        });
        
        // Ensure smooth playback
        video.addEventListener('loadeddata', function() {
            this.currentTime = 0;
        });
    });
    
    // Smooth video transition function
    function transitionToNextVideo() {
        const currentVideo = videos[currentVideoIndex];
        const nextIndex = (currentVideoIndex + 1) % videos.length;
        const nextVideo = videos[nextIndex];
        
        // Prepare next video
        nextVideo.currentTime = 0;
        nextVideo.play().catch(e => console.log('Video play failed:', e));
        
        // Smooth transition
        nextVideo.style.opacity = '0';
        nextVideo.style.display = 'block';
        
        // Fade transition
        let opacity = 0;
        const fadeInterval = setInterval(() => {
            opacity += 0.02;
            nextVideo.style.opacity = opacity;
            currentVideo.style.opacity = 1 - opacity;
            
            if (opacity >= 1) {
                clearInterval(fadeInterval);
                currentVideo.style.opacity = '0';
                currentVideo.classList.remove('active');
                currentVideo.pause();
                
                nextVideo.style.opacity = '1';
                nextVideo.classList.add('active');
                
                currentVideoIndex = nextIndex;
            }
        }, 16); // 60fps
    }
    
    // Auto-rotate videos every 15 seconds
    setInterval(transitionToNextVideo, 15000);
}

// Animated statistics counters
function initializeStatsCounters() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const target = parseInt(entry.target.getAttribute('data-target'));
                animateCounter(entry.target, target);
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.7 });
    
    statNumbers.forEach(stat => observer.observe(stat));
}

function animateCounter(element, target) {
    let current = 0;
    const increment = target / 100;
    const timer = setInterval(() => {
        current += increment;
        element.textContent = Math.floor(current);
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        }
    }, 20);
}

// Testimonial slider
function initializeTestimonialSlider() {
    if (typeof Swiper !== 'undefined') {
        const testimonialSwiper = new Swiper('.testimonialSwiper', {
            slidesPerView: 1,
            spaceBetween: 30,
            loop: true,
            autoplay: {
                delay: 5000,
                disableOnInteraction: false,
            },
            pagination: {
                el: '.swiper-pagination',
                clickable: true,
            },
            navigation: {
                nextEl: '.swiper-button-next',
                prevEl: '.swiper-button-prev',
            },
            breakpoints: {
                768: {
                    slidesPerView: 2,
                },
                1024: {
                    slidesPerView: 3,
                }
            }
        });
    }
}

// Gallery 3D effects
function initializeGalleryEffects() {
    // 3D cube rotation
    const galleryCube = document.querySelector('.gallery-cube');
    if (galleryCube && typeof gsap !== 'undefined') {
        gsap.to(galleryCube, {
            rotationY: 360,
            duration: 20,
            ease: 'none',
            repeat: -1
        });
        
        // Floating animation
        gsap.to(galleryCube, {
            y: -30,
            duration: 3,
            ease: 'power2.inOut',
            repeat: -1,
            yoyo: true
        });
    }
    
    // Gallery item hover effects
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach(item => {
        item.addEventListener('mouseenter', function() {
            if (typeof gsap !== 'undefined') {
                gsap.to(this, { scale: 1.05, duration: 0.3 });
                gsap.to(this.querySelector('img'), { scale: 1.1, duration: 0.3 });
            }
        });
        
        item.addEventListener('mouseleave', function() {
            if (typeof gsap !== 'undefined') {
                gsap.to(this, { scale: 1, duration: 0.3 });
                gsap.to(this.querySelector('img'), { scale: 1, duration: 0.3 });
            }
        });
    });
}

// ===== UTILITY FUNCTIONS =====

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
    `;
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-hide after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Debounce function
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

// Throttle function
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Device detection
const isMobile = /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent);
const isTablet = /(ipad|tablet|(android(?!.*mobile))|(windows(?!.*phone)(.*touch))|kindle|playbook|silk|(puffin(?!.*(IP|AP|WP))))/i.test(navigator.userAgent);

// Export for use in other scripts
window.PhotographyPortfolio = {
    showNotification,
    debounce,
    throttle,
    isMobile,
    isTablet
};

// Add some CSS animations via JavaScript
const style = document.createElement('style');
style.textContent = `
    @keyframes float-particle {
        0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
        10% { opacity: 1; }
        90% { opacity: 1; }
        100% { transform: translateY(-100px) rotate(360deg); opacity: 0; }
    }
    
    .lazy {
        filter: blur(5px);
        transition: filter 0.3s;
    }
    
    .lazy.loaded {
        filter: blur(0);
    }
`;
document.head.appendChild(style);

console.log('🚀 3D Cinematic Photography Portfolio JavaScript Loaded!'); 