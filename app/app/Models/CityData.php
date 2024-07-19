<?php

namespace App\Models;

use MongoDB\Laravel\Eloquent\Model;

class CityData extends Model
{
    protected $connection = 'mongodb';
    protected $collection = 'cityData';
}
