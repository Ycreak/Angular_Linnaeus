
/**
 * This class represents a Fragment column, which contains meta data about a column. Most
 * important within a column is the Fragments object, which is a list containing fragments.
 * This class is also used to pass to api request functions as a pass by reference object.
 * It is also used by the playground and the dashboard.
 */
export class Sandbox
{

    constructor( column? : Partial<Sandbox> )
    {
        // Allow the partial initialisation of a fragment object
        Object.assign( this, column );     
    }

//     "id": 0,
//     "project_title": "Agromyzidae of the World",
//     "project_url": "http://agromyzidae.linnaeus.naturalis.nl",
//     "content": []
//   }

    public id = ''
    public title = ''
    public url = ''
    public introduction = []
    public index = []
    public animals = []



}

