<?php

namespace App\Http\Controllers;

use Inertia\Inertia;
use Illuminate\Support\Facades\Route;
use Illuminate\Foundation\Application;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\File;
use Illuminate\Http\Request;

class IndexController extends Controller
{
    public function getLogs(Request $request)
    {
        if (!$request->user()->is_admin) {
            return response()->json(['error' => 'Unauthorized'], 403);
        }
        $filePath = env('APP_ENV') === 'production' ? '/var/startup.log' : '/Users/user/wac/msc/homepedia/startup.log';

        // Check if the log file exists
        if (!File::exists($filePath)) {
            return response()->json(['error' => 'Log file not found.'], 404);
        }

        // Read the contents of the log file
        $logs = File::get($filePath);

        // Optionally, you can split the logs by line
        $logs = explode("\n", $logs);

        return response()->json(['logs' => $logs], 200);
    }

    private function getDepartements()
    {
        $departments = DB::table('departements')
            ->leftJoin(DB::raw(
                '
                (
                    SELECT DISTINCT ON (LEFT(code_postal, LENGTH(code_postal) - 3)) code_postal, latitude, longitude
                    FROM cartography
                    ORDER BY LEFT(code_postal, LENGTH(code_postal) - 3), code_postal
                ) as c'
            ), function ($join) {
                $join->on(DB::raw('CASE
                    WHEN LEFT(c.code_postal, 2) = \'97\' THEN LEFT(c.code_postal, 3)
                    WHEN LEFT(c.code_postal, 1) = \'0\' THEN RIGHT(LEFT(c.code_postal, 2), 1)
                    ELSE LEFT(c.code_postal, 2)
                END'), '=', DB::raw('CASE
                    WHEN LEFT(departements.num_dep, 2) = \'97\' THEN departements.num_dep
                    ELSE LPAD(departements.num_dep, 2, \'0\')
                END'));
            })
            ->leftJoin('schools', function ($join) {
                $join->on(DB::raw('CASE
                    WHEN LEFT(schools.postal_code, 2) = \'97\' THEN LEFT(schools.postal_code, 3)
                    WHEN LEFT(schools.postal_code, 1) = \'0\' THEN RIGHT(LEFT(schools.postal_code, 2), 1)
                    ELSE LEFT(schools.postal_code, 2)
                END'), '=', DB::raw('CASE
                    WHEN LEFT(departements.num_dep, 2) = \'97\' THEN departements.num_dep
                    ELSE LPAD(departements.num_dep, 2, \'0\')
                END'));
            })
            ->select('departements.*', 'c.latitude', 'c.longitude', DB::raw('COUNT(schools.id) as school_count'))
            ->groupBy('departements.id', 'c.latitude', 'c.longitude')
            ->get();

        return $departments;
    }

    private function getCities()
    {
        $cities = DB::table('cartography')
            ->select('nom_commune_postal', 'latitude', 'longitude', 'code_postal', 'average_cost', 'safety_rate')
            ->get();
        return $cities;
    }

    public function index()
    {
        $departments = $this->getDepartements();
        $cities = $this->getCities();
        return Inertia::render('Index', [
            'departments' => $departments,
            'cities' => $cities,
            'canLogin' => Route::has('login'),
            'canRegister' => Route::has('register'),
            'laravelVersion' => Application::VERSION,
            'phpVersion' => PHP_VERSION,
        ]);
    }
}
