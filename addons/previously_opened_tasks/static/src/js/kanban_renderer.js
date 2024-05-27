/** @odoo-module */

import {patch} from '@web/core/utils/patch';
import {KanbanRenderer} from "@web/views/kanban/kanban_renderer";
import {NeokPOTRenderer} from "./renderer";

patch(KanbanRenderer.prototype, 'previously_opened_tasks.NeokKanbanRenderer', NeokPOTRenderer);