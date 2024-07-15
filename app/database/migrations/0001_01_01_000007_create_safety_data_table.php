<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateSafetyDataTable extends Migration
{
    public function up()
    {
        Schema::create('safety_data', function (Blueprint $table) {
            $table->id();
            $table->integer('annee')->nullable();
            $table->string('classe')->nullable();
            $table->string('unite_de_compte')->nullable();
            $table->decimal('valeur_publiee', 15, 2)->nullable();
            $table->integer('faits')->nullable();
            $table->string('nom_commune')->nullable();
            $table->string('code_postal')->nullable();
            $table->decimal('tauxpourmille', 20, 10)->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('safety_data');
    }
}
