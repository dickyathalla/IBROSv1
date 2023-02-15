<?php
    require 'koneksi.php';

    $hasil = mysqli_query($con, 'SELECT * FROM table_webgis');

    $data = [];
    while ($d = mysqli_fetch_assoc($hasil)){
        $data[] = $d;
    }
    
?>
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="utf-8" />
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
        <meta name="description" content="" />
        <meta name="author" content="" />
        <title>I-BROS | WebGIS</title>
        <!-- Favicon-->
        <link rel="icon" type="image/x-icon" href="assets/favicon.ico" />
        <!-- Core theme CSS (includes Bootstrap)-->
        <link href="css/styles.css" rel="stylesheet" />
        <link href="css/map.css" rel="stylesheet" />
        <!-- leafletjs -->
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.8.0/dist/leaflet.css" integrity="sha512-hoalWLoI8r4UszCkZ5kL8vayOGVae1oxXe/2A4AO6J9+580uKHDO3JdHb7NzwwzK5xr/Fs0W40kiNHxM9vyTtQ==" crossorigin="" />
        <script src="https://unpkg.com/leaflet@1.8.0/dist/leaflet.js" integrity="sha512-BB3hKbKWOc9Ez/TAwyWxNXeoV9c1v6FIeYiBieIWkpLjauysF18NzgR1MBNBXf8/KABdlkX68nAhlwcDFLGPCQ==" crossorigin=""></script>

    </head>
    <body>
        <div class="d-flex" id="wrapper">
            <!-- Sidebar-->
            <div class="border-end bg-white" id="sidebar-wrapper">
                <div class="sidebar-heading border-bottom bg-light">I-BROS</div>
                <div class="list-group list-group-flush">
                    <a class="list-group-item list-group-item-action list-group-item-light p-3" href="index.php">Dashboard</a>
                    <!-- <a class="list-group-item list-group-item-action list-group-item-light p-3" href="data.php">Data</a> -->
                    <!-- <a class="list-group-item list-group-item-action list-group-item-light p-3" href="#">Setting</a> -->
                    <!-- <a class="list-group-item list-group-item-action list-group-item-light p-3" href="#">Sign Up</a> -->
                </div>
            </div>
            <!-- Page content wrapper-->
            <div id="page-content-wrapper">
                <!-- Top navigation-->
                <nav class="navbar navbar-expand-lg navbar-light bg-light border-bottom">
                    <div class="container-fluid">
                        <button class="btn btn-primary" id="sidebarToggle"><</button>
                        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"><span class="navbar-toggler-icon"></span></button>
                        <div class="collapse navbar-collapse" id="navbarSupportedContent">
                            <ul class="navbar-nav ms-auto mt-2 mt-lg-0">
                                <li class="nav-item active"><a class="nav-link" href="#!">Home</a></li>
                                <li class="nav-item dropdown">
                                    <a class="nav-link dropdown-toggle" id="navbarDropdown" href="#" role="button" data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Dropdown</a>
                                    <div class="dropdown-menu dropdown-menu-end" aria-labelledby="navbarDropdown">
                                        <a class="dropdown-item" href="#!">Action</a>
                                        <a class="dropdown-item" href="#!">Another action</a>
                                        <div class="dropdown-divider"></div>
                                        <a class="dropdown-item" href="#!">Something else here</a>
                                    </div>
                                </li>
                            </ul>
                        </div>
                    </div>
                </nav>
                <!-- Page content-->
                <div class="container-fluid">
                    <div id="map">

                    </div>
                </div>
            </div>
        </div>
        <!-- Bootstrap core JS-->
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
        <!-- Core theme JS-->
        <script src="js/scripts.js"></script>
        <!-- lealfetjs -->
        <script>
            getLocation();

            function getLocation() {
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(showPosition);
                }
            }

            function showPosition(position){
                let lat = position.coords.latitude;
                let long = position.coords.longitude

                var map = L.map('map', {
                    center: [lat,long],
                    zoom: 16
                });

                let data = <?php echo json_encode($data); ?>;

                data.map(function(d){
                    L.marker([ d.latitude, d.longitude]).addTo(map).bindPopup(`
                    <p>
                        <b>Tanggal</b>: ${d.created}<br>
                        <b>Latitude</b>: ${d.latitude}<br>
                        <b>Longitude</b>: ${d.longitude}<br>
                        <b>
                        ${d.photo}
                    </p>
                `);    
                })

                console.log(data);

                L.marker([ lat, long], {icon: redIcon})
                .addTo(map).bindPopup(`
                    <p>
                        <b>Your Location</b><br>
                        <b>Latitude</b>: ${lat}<br>
                        <b>Longitude</b>: ${long}
                    </p>
                `);

                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png?{foo}', {foo: 'bar', attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'}).addTo(map);
            }
            
            var redIcon = L.icon({
                iconUrl: 'icon/red.png',

                iconSize:     [38, 40], // size of the iconAnchor
});


        </script>
    </body>
</html>
