<?php $files_names = scandir('./saves/'); ?>

<?php if (!isset($_SERVER['CONTENT_TYPE']) || $_SERVER['CONTENT_TYPE'] !== 'application/json') : ?>
    <!DOCTYPE html>
    <html lang="fr">

    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">

        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Roboto&display=swap" rel="stylesheet">

        <link rel="icon" href="/img/favicon.png" />
        <link rel="stylesheet" href="style.css">

        <title>Database saver</title>
    </head>

    <?php
    setLocale(LC_TIME, 'fr_FR');
    date_default_timezone_set('Europe/Paris');

    $DATE_FORMAT = 'Y-m-d H:i';

    foreach ($files_names as $file_path) {
        if (strpos($file_path, '.zip') > 0) {
            $file['path'] = $file_path;
            $file['name'] = str_replace('.zip', '', $file_path);
            $file['formated_name'] = DateTime::createFromFormat($DATE_FORMAT, $file['name'])->format('d/m/Y H:i');

            $splited_name = explode(' ', $file['name']);

            $date_formated = DateTime::createFromFormat('Y-m-d', $splited_name[0])->format('d/m/Y');

            $files[$date_formated][] = $file;
            $dates[] = $date_formated;
        }
    }

    $dates = array_unique($dates);
    $dates = array_reverse($dates);

    $last_date_formated = DateTime::createFromFormat($DATE_FORMAT, $files[$dates[0]][count($files[$dates[0]]) - 1]['name'])->format('d/m/Y \à H:i');
    ?>

    <body>
        <h1 class="mb-0">Sauvegarde de base de données</h1>
        <p class="mt-0">Dernière sauvegarde le <?= $last_date_formated; ?></p>
        <?php foreach ($dates as $date) : ?>
            <div class="backup-files-day">
                <h2 class="mb-0 font-1-3">Sauvegarde<?= count($files[$date]) > 1 ? 's' : ''; ?> du <?= $date; ?></h2>
                <div class="row">
                    <?php foreach ($files[$date] as $file) : ?>
                        <a class="file file-link" href="/saves/<?= $file['path'] ?>">
                            <img class="file-image" src="/img/zip.png" alt="">
                            <p class="file-name"><?= $file['formated_name']; ?></p>
                        </a>
                    <?php endforeach; ?>
                </div>
            </div>
            <hr>
        <?php endforeach; ?>
    </body>

    </html>
<?php
else :
    foreach ($files_names as $file_path) {
        if (strpos($file_path, '.zip') > 0) {
            $data[] = "/saves/" . $file_path;
        }
    }

    echo json_encode(['code' => 200, 'status' => 'OK', 'data' => $data], JSON_UNESCAPED_SLASHES);
endif; ?>