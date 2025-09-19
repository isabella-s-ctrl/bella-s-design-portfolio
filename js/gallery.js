// Gallery filtering for fun-stuff page
document.addEventListener('DOMContentLoaded', function() {
    console.log('Gallery script loaded');
    
    const filterButtons = document.querySelectorAll('.filter-btn');
    const galleryItems = document.querySelectorAll('.gallery-item');
    
    console.log('Found filter buttons:', filterButtons.length);
    console.log('Found gallery items:', galleryItems.length);

    filterButtons.forEach(button => {
        button.addEventListener('click', () => {
            console.log('Button clicked:', button.getAttribute('data-filter'));
            
            // Remove active class from all buttons
            filterButtons.forEach(btn => btn.classList.remove('active'));
            // Add active class to clicked button
            button.classList.add('active');
            
            const filterValue = button.getAttribute('data-filter');
            
            galleryItems.forEach(item => {
                const itemCategory = item.getAttribute('data-category');
                console.log('Item category:', itemCategory, 'Filter value:', filterValue);
                
                if (filterValue === 'all' || itemCategory === filterValue) {
                    item.style.display = 'block';
                    item.style.animation = 'fadeIn 0.5s ease';
                } else {
                    item.style.display = 'none';
                }
            });
        });
    });
});

// Add fadeIn animation (scoped variable to avoid global collisions)
const galleryStyle = document.createElement('style');
galleryStyle.textContent = `
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(20px); }
        to { opacity: 1; transform: translateY(0); }
    }
`;
document.head.appendChild(galleryStyle);