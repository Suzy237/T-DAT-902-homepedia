<?php

namespace App\Http\Controllers;

use Inertia\Inertia;
use Illuminate\Support\Facades\Route;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\DB;

class IndexController extends Controller
{

    private function getDepartements()
    {
        $departments = DB::table('departements')
            ->leftJoin(DB::raw('(SELECT DISTINCT ON (LEFT(code_postal, LENGTH(code_postal) - 3)) code_postal, latitude, longitude FROM cartography WHERE RIGHT(code_postal, 3) = \'000\') as c'), 'departements.num_dep', '=', DB::raw('LEFT(c.code_postal, LENGTH(departements.num_dep))'))
            ->select('departements.*', 'c.latitude', 'c.longitude')
            ->get();
        return $departments;
    }

    public function index()
    {
        $departments = $this->getDepartements();
        return Inertia::render('Index', [
            'departments' => $departments,
            'canLogin' => Route::has('login'),
            'canRegister' => Route::has('register'),
            'laravelVersion' => Application::VERSION,
            'phpVersion' => PHP_VERSION,
        ]);
    }
}
