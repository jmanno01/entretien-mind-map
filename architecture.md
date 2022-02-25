# Mind map concept, web services

## Context: Human brain
### Goal: Obtain informations of the humain brain trait (left side and right side)

- [**Brain Trait**]
    - [Logical]
        - [aplying sunscreen will prevent sunburn]
        - [breathing keep you alive]
    - [Focus on facts]
        - [lay out the problem]
        - [become knowledgeable about the situation]
    - [Realism predominates]
        - [knowing our own limitation in regard to travel into space]
    - [Planned and ordely]
        - [should the proposal be proceed]
    - [Math and science minded]
        - [algebraic balance is required in chemical formulas]
    - [Prefers nonfiction]
        - [provide an anchor in the real world]

    - [Emotional]
        - [been happy]
         - [crying for the lost ones]
    - [Focused on art and creativity]
        - [monalisa painting is beautiful]
    - [Imagination predominates]
        - [there is a monster under the bed, papa]
    - [Occasionally absentminded]
        - [oups I did it again]
    - [Prefers fiction]
        - [harry potter books are such wonderfull stories]
    - [Enjoys creative storytelling]
        - [valentine's day is a beautiful story]
        
## Procedure

1. Provide Human Brain trait web service endpoint
2. Collection -> multiples resources of the same type -> brain trait
3. The method in regard to the Resources -> `create(POST)` resource, `retrieve(GET)` resource and `delete(DELETE)`resource
4. Resource -> object that the API store -> information of the brain trait for the Left and right side
5. Ability to create the method will be expose over the `REST API`

### Endpoint
1. Collection: /brainTrait
    - `GET` -> view collection
    - `POST` -> create new resource
    
2. Ressource: /brainTrait/identifier 
    - `GET` -> view collection
    - `DELETE` -> delete resource

### Usage
- Responses will be represented in json format
```json
{   
    "data": "Mixed type holding the content of the response",
    "message": "Description of what happened"   
}
```

- Subsequent response definitions will only detail the expected value of the `data field`
### List all brain traits
`GET /brainTrait` 
### Response
`200 OK` on success

```json
[   
    {
        "identifier": "Logical",
        "path": "path/to/logical",
        "text": "aplying sunscreen will prevent sunburn"
    },
    {
        "identifier": "Emotional",
        "path": "path/to/emotional",
        "text": "been happy"
    } 
]
```

### Registering a new 
`POST /brainTrait` 

### Arguments
- `"identifier": string`, identifier for the mind map
- `"path": string` a path for the brain trait 
- `"text": string` short sentence illustrating the trait 

if a brain trait with given identifier already exists, it will be overwritten
### Response
`201 Created` on success
```json
   {
        "identifier": "Logical",
        "path": "path/to/logical",
        "text": "aplying sunscreen will prevent sunburn"
    }
```

## Lookup brain trait details
`GET /brainTrait/identifier`
### Response 
- `404 Not Foud` if brain trait does not exist 
- `200 OK` on success
```json
  {
        "identifier": "Logical",
        "path": "path/to/logical",
        "text": "aplying sunscreen will prevent sunburn"
    }
```

### Delete brain trait
`DELETE /brainTrait/identifier`
### Response
- `404 NOT FOUND` if brain trait does not exist 
- `204` no content