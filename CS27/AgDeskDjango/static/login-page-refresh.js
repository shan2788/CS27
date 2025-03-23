(function() {
    // Function to force refresh the page
    function forceRefresh() {
        window.location.reload(true);
    }

    // Listen for the 'pageshow' event
    window.addEventListener('pageshow', function(event) {
        // Check if the page is being loaded from the bfcache (back-forward cache)
        if (event.persisted) {
            forceRefresh();
        }
    });

    // Additional check using the Performance API
    if (window.performance && window.performance.navigation) {
        if (window.performance.navigation.type === window.performance.navigation.TYPE_BACK_FORWARD) {
            forceRefresh();
        }
    }

    // For modern browsers that support the Navigation API
    if (window.navigation) {
        if (window.navigation.type === 'back-forward') {
            forceRefresh();
        } else {
            window.navigation.addEventListener('navigate', (event) => {
                if (event.navigationType === 'back-forward') {
                    forceRefresh();
                }
            });
        }
    }
})();