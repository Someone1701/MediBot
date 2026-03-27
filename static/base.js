// Dashboard functionality
function toggleDashboard() {
    const dashboard = document.getElementById('dashboardMenu');
    const overlay = document.getElementById('dashboardOverlay');

    dashboard.classList.toggle('active');
    overlay.classList.toggle('active');
}

function closeDashboard() {
    const dashboard = document.getElementById('dashboardMenu');
    const overlay = document.getElementById('dashboardOverlay');

    dashboard.classList.remove('active');
    overlay.classList.remove('active');
}

// Close dashboard with Escape key
document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') {
        closeDashboard();
    }
});

// Sample AI responses for demo
const aiResponses = [
    "I understand your concern. Based on what you've described, here are some general recommendations. However, for a proper diagnosis, I'd recommend consulting with a healthcare provider.",
    "That's a great question about your health! Let me provide you with some evidence-based information that might help.",
    "Thank you for sharing that information. Based on current medical guidelines, here's what I can tell you about your symptoms.",
    "I'd be happy to help you understand more about this condition. Here's some reliable health information from trusted medical sources.",
    "For your safety, I recommend speaking with a licensed healthcare provider about this concern. Would you like me to help you schedule a video consultation?"
];

function sendMessage() {
    const input = document.getElementById('messageInput');
    const messages = document.getElementById('chatMessages');

    if (input.value.trim() === '') return;

    // Add user message
    const userMessage = document.createElement('div');
    userMessage.className = 'message user';
    userMessage.innerHTML = `<p>${input.value}</p>`;
    ;
    messages.appendChild(userMessage);

    // Clear input
    const userText = input.value;
    input.value = '';

    // Simulate AI response after a delay
    setTimeout(() => {
        const aiMessage = document.createElement('div');
        aiMessage.className = 'message ai';
        const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)];
        aiMessage.innerHTML = `<p>${randomResponse}</p>`;
        ;
        messages.appendChild(aiMessage);

        // Scroll to bottom
        messages.scrollTop = messages.scrollHeight;
    }, 1000 + Math.random() * 1000);

    // Scroll to bottom
    messages.scrollTop = messages.scrollHeight;
}

// Allow Enter key to send message
document.getElementById('messageInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

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

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver(function (entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards
document.querySelectorAll('.feature-card').forEach(card => {
    card.style.opacity = '0';
    card.style.transform = 'translateY(20px)';
    card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
    observer.observe(card);
});