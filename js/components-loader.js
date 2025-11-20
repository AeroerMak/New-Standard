/**
 * Dynamic Header and Footer Loader
 * Loads header and footer components into pages dynamically
 */

(function() {
    'use strict';

    // Configuration
    const CONFIG = {
        headerPath: 'components/header.html',
        footerPath: 'components/footer.html',
        headerSelector: '#header-placeholder',
        footerSelector: '#footer-placeholder'
    };

    /**
     * Load a component from an HTML file
     * @param {string} path - Path to the HTML file
     * @param {string} selector - CSS selector where to insert the content
     * @param {Function} callback - Optional callback function after loading
     */
    function loadComponent(path, selector, callback) {
        const element = document.querySelector(selector);
        
        if (!element) {
            console.warn('Component loader: Element not found for selector:', selector);
            return;
        }

        fetch(path)
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.text();
            })
            .then(html => {
                element.innerHTML = html;
                
                // Note: Menu initialization will be handled by waitForJQuery function below
                
                if (callback) {
                    callback();
                }
            })
            .catch(error => {
                console.error('Error loading component:', path, error);
                element.innerHTML = '<div style="color: red; padding: 20px;">Error loading component: ' + path + '</div>';
            });
    }

    /**
     * Initialize component loading
     */
    function init() {
        // Load header
        loadComponent(CONFIG.headerPath, CONFIG.headerSelector, function() {
            console.log('Header loaded successfully');
        });

        // Load footer
        loadComponent(CONFIG.footerPath, CONFIG.footerSelector, function() {
            console.log('Footer loaded successfully');
        });
    }

    /**
     * Wait for jQuery to be available, then initialize menu
     */
    function waitForJQuery(callback) {
        if (typeof jQuery !== 'undefined') {
            callback();
        } else {
            setTimeout(function() {
                waitForJQuery(callback);
            }, 50);
        }
    }

    // Wait for DOM to be ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        // DOM is already ready
        init();
    }

    // Wait for jQuery and menu.js to initialize mobile menu after header loads
    waitForJQuery(function() {
        // This will be called after header is loaded and jQuery is available
        setTimeout(function() {
            if (typeof jQuery !== 'undefined') {
                jQuery(document).ready(function($) {
                    // Re-initialize mobile menu if header is loaded
                    if ($("#menu_border_wrapper").length > 0 && $("#menu_border_wrapper select").length === 0) {
                        $("<select />").appendTo("#menu_border_wrapper");
                        
                        $("<option />", {
                            "selected": "selected",
                            "value": "",
                            "text": "Menu"
                        }).appendTo("#menu_border_wrapper select");
                        
                        $(".nav a").each(function() {
                            var el = $(this);
                            $("<option />", {
                                "value": el.attr("href"),
                                "text": el.text()
                            }).appendTo("#menu_border_wrapper select");
                        });
                        
                        $("#menu_border_wrapper select").change(function() {
                            window.location = $(this).find("option:selected").val();
                        });
                    }
                });
            }
        }, 500);
    });

    // Export for external use if needed
    window.ComponentLoader = {
        loadComponent: loadComponent,
        init: init
    };

})();

