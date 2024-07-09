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
            $table->string('code_commune_INSEE')->nullable();
            $table->string('nom_commune_postal')->nullable();
            $table->string('code_postal')->nullable();
            $table->string('libelle_acheminement')->nullable();
            $table->decimal('latitude', 10, 8)->nullable();
            $table->decimal('longitude', 11, 8)->nullable();
            $table->string('nom_region')->nullable();
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
