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
            $table->date('mutation_date')->nullable();
            $table->string('nature_mutation')->nullable();
            $table->decimal('valeur_fonciere', 15, 2)->nullable();
            $table->string('address')->nullable();
            $table->string('postal_code')->nullable();
            $table->string('commune')->nullable();
            $table->string('department_code')->nullable();
            $table->string('commune_code')->nullable();
            $table->decimal('surface_reelle_bati', 10, 2)->nullable();
            $table->integer('nombre_pieces')->nullable();
            $table->decimal('surface_terrain', 10, 2)->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('real_estate');
    }
}
