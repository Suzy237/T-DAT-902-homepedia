<?php

use App\Http\Controllers\ProfileController;
use App\Http\Controllers\DataController;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\Route;
use Inertia\Inertia;
use App\Http\Controllers\IndexController;
use App\Http\Controllers\MapDataController;

Route::get('/', [IndexController::class, 'index'])->name('home');

Route::get('/departments', [MapDataController::class, 'getDepartments']);
Route::get('/cities', [MapDataController::class, 'getCities']);
Route::get('/location/{id}', [MapDataController::class, 'getLocationDetails']);
Route::get('/city/{id}', [MapDataController::class, 'getCityDataFromMongoDB']);
Route::get('/cities/{name}', [MapDataController::class, 'findCitiesByName']);

Route::get('/dashboard', function () {
    return Inertia::render('Dashboard');
})->middleware(['auth', 'verified'])->name('dashboard');

Route::middleware('auth')->group(function () {
    Route::get('/profile', [ProfileController::class, 'edit'])->name('profile.edit');
    Route::patch('/profile', [ProfileController::class, 'update'])->name('profile.update');
    Route::delete('/profile', [ProfileController::class, 'destroy'])->name('profile.destroy');
});

Route::middleware('auth')->group(function () {
    Route::get('/fetch-csvs', [DataController::class, 'fetchCsvs']);
    Route::get('/process-data', [DataController::class, 'processData']);
});

require __DIR__ . '/auth.php';
