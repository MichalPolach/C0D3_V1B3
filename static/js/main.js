/**
 * Main JavaScript for C0D3_V1B3
 * ============================
 * This script handles interactive elements for the blog:
 * - Mobile menu toggling for responsive design
 * - Auto-dismissing notification messages
 * - Copy buttons for code blocks to enhance user experience
 */

document.addEventListener('DOMContentLoaded', function() {
    // =========================================
    // Mobile Menu Functionality
    // =========================================
    const menuToggle = document.querySelector('.menu-toggle');
    const mainNav = document.querySelector('.main-nav');
    
    if (menuToggle && mainNav) {
        // Toggle mobile menu visibility when hamburger icon is clicked
        menuToggle.addEventListener('click', function() {
            mainNav.style.display = mainNav.style.display === 'block' ? 'none' : 'block';
        });
        
        // Reset menu display when window is resized above mobile breakpoint
        // This prevents the menu from staying hidden when switching from mobile to desktop view
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                mainNav.style.display = '';
            }
        });
    }
    
    // =========================================
    // Message Alert Auto-Dismissal
    // =========================================
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function(alert) {
        // Fade out alerts after 4 seconds
        setTimeout(function() {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            
            // Remove from DOM after fade animation completes
            setTimeout(function() {
                alert.style.display = 'none';
            }, 500);
        }, 4000);
    });

    // Add copy functionality to code blocks
    addCopyCodeButtons();
});

/**
 * Adds "Copy" buttons to all code blocks in the page
 * 
 * This function finds all <pre><code> elements and adds a button
 * that allows users to copy the code to their clipboard with one click.
 * It also handles visual feedback for the copy action.
 */
function addCopyCodeButtons() {
    // Find all code blocks
    const codeBlocks = document.querySelectorAll('pre code');
    
    // Process each code block
    codeBlocks.forEach((codeBlock) => {
        // Create the copy button element
        const copyButton = document.createElement('button');
        copyButton.className = 'copy-code-button';
        copyButton.textContent = 'Copy';
        
        // Set up the code block's parent for positioning
        const parentPre = codeBlock.parentElement;
        parentPre.style.position = 'relative';
        
        // Add click handler to copy the code
        copyButton.addEventListener('click', function() {
            // Get the text content of the code block
            const code = codeBlock.textContent;
            
            // Use the Clipboard API to copy the text
            navigator.clipboard.writeText(code).then(() => {
                // Show success status by changing button text
                copyButton.textContent = 'Copied!';
                
                // Reset button text after 2 seconds
                setTimeout(() => {
                    copyButton.textContent = 'Copy';
                }, 2000);
            });
        });
        
        // Add the button to the code block
        parentPre.appendChild(copyButton);
    });
} 