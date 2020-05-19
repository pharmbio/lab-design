-- Good SQL queries
EXPLAIN (ANALYZE, BUFFERS) SELECT * from images_all_view WHERE plate = 'P009095'

EXPLAIN (ANALYZE, BUFFERS)
SELECT DISTINCT plate, project
FROM images
ORDER BY project, plate

-- list all pg server conf params
SHOW ALL


-- Create database, tables, index, viwes
CREATE DATABASE labdesign;

-- Log in to new database
\c labdesign;


DROP TABLE IF EXISTS "protocols";
CREATE TABLE "public"."protocols" (
    "name" text PRIMARY KEY,
    "steps" jsonb,
    "id" serial
) WITH (oids = false);

CREATE INDEX "ix_protocols_name" ON "public"."protocols" USING btree ("name");

INSERT INTO protocols(name, steps)
VALUES
      (
        'Cellpainting-96-version-1',
        '[
                     { "name": "wash", "protocol": "wash-40uL" },
                     { "name": "disp", "protocol": "disp-40uL-mito" },
                     { "name": "incu_co2", "time": "20" },
                     { "name": "wash", "protocol": "wash-3x-70uL-dye" },
                     { "name": "disp", "protocol": "disp-70uL-PFE" },
                     { "name": "incu_room", "time": "20" },
                     { "name": "wash", "protocol": "wash-40uL" },
                     { "name": "disp", "protocol": "disp-70uL-triton" },
                     { "name": "shake", "time": "17" },
                     { "name": "wash", "protocol": "wash-20uL" },
                     { "name": "disp", "protocol": "disp-50uL-color-cocktail" },
                     { "name": "incu_room", "time": "20" },
                     { "name": "wash", "protocol": "wash-3x-80uL-dye" },
                     { "name": "cool", "time": "forever" }
         ]'
       );

INSERT INTO protocols(name, steps)
VALUES
      (
        'Cellpainting-96-version-2',
        '[
                     { "name": "wash", "protocol": "wash-20uL" },
                     { "name": "disp", "protocol": "disp-20uL-mito" },
                     { "name": "incu_co2", "time": "20" },
                     { "name": "wash", "protocol": "wash-3x-70uL-dye" },
                     { "name": "disp", "protocol": "disp-70uL-PFE" },
                     { "name": "incu_room", "time": "20" },
                     { "name": "wash", "protocol": "wash-20uL" },
                     { "name": "disp", "protocol": "disp-70uL-triton" },
                     { "name": "shake", "time": "17" },
                     { "name": "wash", "protocol": "wash-20uL" },
                     { "name": "disp", "protocol": "disp-50uL-color-cocktail" },
                     { "name": "incu_room", "time": "20" },
                     { "name": "wash", "protocol": "wash-3x-80uL-dye" }
         ]'
       );