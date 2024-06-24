<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateRealEstateTable extends Migration
{
    public function up()
    {
        Schema::create('real_estate', function (Blueprint $table) {
            $table->id();
            $table->date('mutation_date');
            $table->string('nature_mutation');
            $table->decimal('valeur_fonciere', 15, 2);
            $table->string('address');
            $table->string('postal_code');
            $table->string('commune');
            $table->string('department_code');
            $table->string('commune_code');
            $table->decimal('surface_reelle_bati', 10, 2);
            $table->integer('nombre_pieces');
            $table->decimal('surface_terrain', 10, 2);
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('real_estate');
    }
}
