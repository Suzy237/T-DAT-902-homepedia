<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateSchoolsTable extends Migration
{
    public function up()
    {
        Schema::create('schools', function (Blueprint $table) {
            $table->id();
            $table->string('identifiant');
            $table->string('nom_etablissement');
            $table->string('type_etablissement');
            $table->string('statut_public_prive');
            $table->string('address');
            $table->string('postal_code');
            $table->string('commune');
            $table->string('department_code');
            $table->string('region_code');
            $table->integer('nombre_eleves');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('schools');
    }
}
