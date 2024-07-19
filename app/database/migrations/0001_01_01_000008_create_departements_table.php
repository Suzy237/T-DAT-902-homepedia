<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateDepartementsTable extends Migration
{
    public function up()
    {
        Schema::create('departements', function (Blueprint $table) {
            $table->id();
            $table->string('num_dep')->unique();
            $table->string('dep_name');
            $table->string('region_name');
            $table->timestamps();
        });
    }

    public function down()
    {
        Schema::dropIfExists('departements');
    }
}
