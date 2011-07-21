<VirtualHost *:80>
    ServerName %(host)s
    ServerAdmin %(admin)s
    DocumentRoot %(root_dir)s

    <Directory "%(root_dir)s">
        Order allow,deny
        Allow from All
        Options Includes ExecCGI FollowSymLinks
        AddHandler cgi-script .cgi .pl .py .rb
        DirectoryIndex index.html index.cgi index.php index.pl index.py index.rb
        AllowOverride All
    </Directory>
</VirtualHost>
