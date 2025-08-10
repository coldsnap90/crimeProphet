
   document.addEventListener('DOMContentLoaded', function () {
       // Auto-dismiss alerts after 3 seconds
       setTimeout(function() {
           var alerts = document.querySelectorAll('.alert');
           alerts.forEach(function(alert) {
               alert.style.opacity = 0;
               setTimeout(function() {
                   alert.remove();
               }, 600); // match this duration with the CSS transition
           });
       }, 3000);
   });
