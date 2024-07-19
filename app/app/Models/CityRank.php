<?php

namespace App\Models;

use MongoDB\Laravel\Eloquent\Model;

class CityRank extends Model
{
    protected $connection = 'mongodb';
    protected $collection = 'cityRank';
}
