-- =====================================================================
-- Fichier : 02_seed.sql — jeu de données FICTIF (40 structures)
-- Les noms, numéros et capacités sont inventés pour la démonstration.
-- =====================================================================

INSERT INTO structures_sanitaires
    (code, nom, type, statut, region, ville, nombre_lits, telephone, services, date_ouverture)
VALUES
-- Centre
('CHU-CEN-001', 'CHU Fictif de Ouagadougou Nord',       'CHU',      'PUBLIC', 'Centre', 'Ouagadougou', 620, '+226 25 00 10 01', '{urgences,chirurgie,maternite,pediatrie,imagerie}', '1985-03-12'),
('CHU-CEN-002', 'CHU Fictif de Ouagadougou Sud',        'CHU',      'PUBLIC', 'Centre', 'Ouagadougou', 480, '+226 25 00 10 02', '{urgences,cardiologie,maternite,laboratoire}',     '1998-06-01'),
('CMA-CEN-001', 'CMA Fictif de Pissy',                  'CMA',      'PUBLIC', 'Centre', 'Ouagadougou',  85, '+226 25 00 11 01', '{urgences,maternite,laboratoire}',                 '2004-01-20'),
('CMA-CEN-002', 'CMA Fictif de Kossodo',                'CMA',      'PUBLIC', 'Centre', 'Ouagadougou',  70, '+226 25 00 11 02', '{maternite,pediatrie}',                           '2007-09-15'),
('CSPS-CEN-001','CSPS Fictif de Tanghin',               'CSPS',     'PUBLIC', 'Centre', 'Ouagadougou',  12, '+226 25 00 12 01', '{consultation,vaccination,maternite}',             '2010-04-03'),
('CSPS-CEN-002','CSPS Fictif de Wemtenga',              'CSPS',     'PUBLIC', 'Centre', 'Ouagadougou',  10, '+226 25 00 12 02', '{consultation,vaccination}',                       '2012-11-22'),
('CLI-CEN-001', 'Clinique Fictive Les Palmiers',        'CLINIQUE', 'PRIVE',  'Centre', 'Ouagadougou',  45, '+226 25 00 13 01', '{chirurgie,imagerie,laboratoire}',                 '2015-02-10'),
('CLI-CEN-002', 'Clinique Fictive Espoir Santé',        'CLINIQUE', 'PRIVE',  'Centre', 'Ouagadougou',  30, '+226 25 00 13 02', '{maternite,pediatrie}',                            '2018-07-08'),
-- Hauts-Bassins
('CHU-HBS-001', 'CHU Fictif de Bobo-Dioulasso',         'CHU',      'PUBLIC', 'Hauts-Bassins', 'Bobo-Dioulasso', 550, '+226 20 00 20 01', '{urgences,chirurgie,maternite,pediatrie,cardiologie}', '1980-10-05'),
('CMA-HBS-001', 'CMA Fictif de Dô',                     'CMA',      'PUBLIC', 'Hauts-Bassins', 'Bobo-Dioulasso',  75, '+226 20 00 21 01', '{urgences,maternite}',                     '2003-05-17'),
('CSPS-HBS-001','CSPS Fictif de Sarfalao',              'CSPS',     'PUBLIC', 'Hauts-Bassins', 'Bobo-Dioulasso',  14, '+226 20 00 22 01', '{consultation,vaccination,maternite}',      '2009-08-30'),
('CSPS-HBS-002','CSPS Fictif de Houndé Centre',         'CSPS',     'PUBLIC', 'Hauts-Bassins', 'Houndé',          10, '+226 20 00 22 02', '{consultation,vaccination}',               '2013-03-14'),
('CLI-HBS-001', 'Clinique Fictive du Houet',            'CLINIQUE', 'PRIVE',  'Hauts-Bassins', 'Bobo-Dioulasso',  38, '+226 20 00 23 01', '{chirurgie,laboratoire}',                  '2016-12-01'),
-- Nord
('CHR-NOR-001', 'CHR Fictif de Ouahigouya',             'CHR',      'PUBLIC', 'Nord', 'Ouahigouya', 260, '+226 24 00 30 01', '{urgences,chirurgie,maternite,pediatrie}', '1992-02-25'),
('CMA-NOR-001', 'CMA Fictif de Yako',                   'CMA',      'PUBLIC', 'Nord', 'Yako',        60, '+226 24 00 31 01', '{maternite,laboratoire}',                  '2006-06-19'),
('CSPS-NOR-001','CSPS Fictif de Gourcy',                'CSPS',     'PUBLIC', 'Nord', 'Gourcy',      10, '+226 24 00 32 01', '{consultation,vaccination}',               '2011-01-09'),
-- Centre-Ouest
('CHR-COU-001', 'CHR Fictif de Koudougou',              'CHR',      'PUBLIC', 'Centre-Ouest', 'Koudougou', 240, '+226 25 40 40 01', '{urgences,chirurgie,maternite}',       '1990-09-12'),
('CMA-COU-001', 'CMA Fictif de Réo',                    'CMA',      'PUBLIC', 'Centre-Ouest', 'Réo',        55, '+226 25 40 41 01', '{maternite,pediatrie}',                '2005-04-27'),
('CSPS-COU-001','CSPS Fictif de Sabou',                 'CSPS',     'PUBLIC', 'Centre-Ouest', 'Sabou',      8,  '+226 25 40 42 01', '{consultation,vaccination}',           '2014-10-02'),
('CLI-COU-001', 'Clinique Fictive Saint-Luc',           'CLINIQUE', 'PRIVE',  'Centre-Ouest', 'Koudougou',  25, '+226 25 40 43 01', '{consultation,laboratoire}',           '2019-05-21'),
-- Est
('CHR-EST-001', 'CHR Fictif de Fada N''Gourma',         'CHR',      'PUBLIC', 'Est', 'Fada N''Gourma', 230, '+226 24 77 50 01', '{urgences,chirurgie,maternite}',      '1991-11-11'),
('CSPS-EST-001','CSPS Fictif de Diapaga',               'CSPS',     'PUBLIC', 'Est', 'Diapaga',         12, '+226 24 77 52 01', '{consultation,vaccination,maternite}', '2008-07-04'),
('CSPS-EST-002','CSPS Fictif de Pama',                  'CSPS',     'PUBLIC', 'Est', 'Pama',             9, '+226 24 77 52 02', '{consultation}',                       '2015-01-16'),
-- Centre-Est
('CHR-CES-001', 'CHR Fictif de Tenkodogo',              'CHR',      'PUBLIC', 'Centre-Est', 'Tenkodogo', 210, '+226 24 71 60 01', '{urgences,maternite,pediatrie}',        '1993-03-08'),
('CMA-CES-001', 'CMA Fictif de Koupéla',                'CMA',      'PUBLIC', 'Centre-Est', 'Koupéla',    65, '+226 24 71 61 01', '{urgences,maternite}',                  '2002-12-13'),
-- Boucle du Mouhoun
('CHR-BMO-001', 'CHR Fictif de Dédougou',               'CHR',      'PUBLIC', 'Boucle du Mouhoun', 'Dédougou', 220, '+226 20 52 70 01', '{urgences,chirurgie,maternite}', '1994-08-22'),
('CSPS-BMO-001','CSPS Fictif de Nouna',                 'CSPS',     'PUBLIC', 'Boucle du Mouhoun', 'Nouna',     11, '+226 20 52 72 01', '{consultation,vaccination}',      '2010-02-18'),
-- Sahel
('CHR-SAH-001', 'CHR Fictif de Dori',                   'CHR',      'PUBLIC', 'Sahel', 'Dori',     180, '+226 24 46 80 01', '{urgences,maternite,pediatrie}', '1996-04-30'),
('CSPS-SAH-001','CSPS Fictif de Djibo',                 'CSPS',     'PUBLIC', 'Sahel', 'Djibo',     10, '+226 24 46 82 01', '{consultation,vaccination}',      '2012-06-06'),
-- Cascades
('CHR-CAS-001', 'CHR Fictif de Banfora',                'CHR',      'PUBLIC', 'Cascades', 'Banfora', 200, '+226 20 91 90 01', '{urgences,chirurgie,maternite}', '1995-07-14'),
('CLI-CAS-001', 'Clinique Fictive de la Comoé',         'CLINIQUE', 'PRIVE',  'Cascades', 'Banfora',  20, '+226 20 91 93 01', '{consultation,maternite}',       '2020-01-27'),
-- Sud-Ouest
('CHR-SOU-001', 'CHR Fictif de Gaoua',                  'CHR',      'PUBLIC', 'Sud-Ouest', 'Gaoua',  190, '+226 20 90 10 01', '{urgences,maternite}',            '1997-10-19'),
('CSPS-SOU-001','CSPS Fictif de Diébougou',             'CSPS',     'PUBLIC', 'Sud-Ouest', 'Diébougou', 9, '+226 20 90 12 01', '{consultation,vaccination}',     '2016-03-03'),
-- Centre-Nord
('CHR-CNO-001', 'CHR Fictif de Kaya',                   'CHR',      'PUBLIC', 'Centre-Nord', 'Kaya',   215, '+226 24 45 20 01', '{urgences,chirurgie,maternite,pediatrie}', '1992-05-05'),
('CMA-CNO-001', 'CMA Fictif de Boulsa',                 'CMA',      'PUBLIC', 'Centre-Nord', 'Boulsa',  50, '+226 24 45 21 01', '{maternite}',                    '2008-11-28'),
-- Plateau-Central
('CMA-PCE-001', 'CMA Fictif de Ziniaré',                'CMA',      'PUBLIC', 'Plateau-Central', 'Ziniaré', 80, '+226 25 30 30 01', '{urgences,maternite,laboratoire}', '2001-09-09'),
('CSPS-PCE-001','CSPS Fictif de Zorgho',                'CSPS',     'PUBLIC', 'Plateau-Central', 'Zorgho',  11, '+226 25 30 32 01', '{consultation,vaccination}',      '2013-08-12'),
-- Centre-Sud
('CHR-CSU-001', 'CHR Fictif de Manga',                  'CHR',      'PUBLIC', 'Centre-Sud', 'Manga', 170, '+226 25 40 50 01', '{urgences,maternite}',               '1999-12-01'),
('CSPS-CSU-001','CSPS Fictif de Pô',                    'CSPS',     'PUBLIC', 'Centre-Sud', 'Pô',     10, '+226 25 40 52 01', '{consultation,vaccination,maternite}', '2011-07-23'),
('CLI-CSU-001', 'Clinique Fictive du Nazinon',          'CLINIQUE', 'PRIVE',  'Centre-Sud', 'Manga',  18, '+226 25 40 53 01', '{consultation}',                     '2021-04-15');
