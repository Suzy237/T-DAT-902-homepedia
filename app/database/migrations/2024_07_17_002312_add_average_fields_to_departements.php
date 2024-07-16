<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('departements', function (Blueprint $table) {
            $table->decimal('average_cost', 15, 2)->nullable();
            $table->decimal('safety_rate', 20, 10)->nullable();
            $table->decimal('avg_valeur_fonciere', 15, 2)->nullable();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('departements', function (Blueprint $table) {
            $table->dropColumn('average_cost');
            $table->dropColumn('safety_rate');
            $table->dropColumn('avg_valeur_fonciere');
        });
    }
};
