<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateCartographyTable extends Migration
{
    public function up()
    {
        Schema::create('cartography', function (Blueprint $table) {
            $table->id();
            $table->string('code_commune_INSEE');
            $table->string('nom_commune_postal');
            $table->string('code_postal');
            $table->string('libelle_acheminement');
            $table->decimal('latitude', 10, 8);
            $table->decimal('longitude', 11, 8);
            $table->string('nom_region');
            $table->timestamps();
        });

        Schema::table('cartography', function (Blueprint $table) {
            $table->index('code_commune_INSEE');
        });
    }

    public function down()
    {
        Schema::dropIfExists('cartography');
    }
}
