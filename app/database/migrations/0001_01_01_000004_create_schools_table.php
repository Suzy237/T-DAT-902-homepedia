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
            $table->string('identifiant')->nullable();
            $table->string('nom_etablissement')->nullable();
            $table->string('type_etablissement')->nullable();
            $table->string('statut_public_prive')->nullable();
            $table->string('address')->nullable();
            $table->string('postal_code')->nullable();
            $table->string('commune')->nullable();
            $table->string('department_code')->nullable();
            $table->string('region_code')->nullable();
            $table->integer('nombre_eleves')->nullable();
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('schools');
    }
}
